import phonenumbers

from fastapi import Depends, Form, HTTPException, APIRouter, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session


from config import app
from worker import (get_user_info_by_username_task, get_user_info_by_email_task, create_user_info_task,
                    phone_validated_task)
from . import models, schemas, crud
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


templates = Jinja2Templates(directory="templates")
router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def phone_validated(phone_number):
    try:
        parsed_phone_number = phonenumbers.parse(phone_number, None)
        return phonenumbers.is_possible_number(parsed_phone_number)
    except phonenumbers.phonenumberutil.NumberParseException:
        return False


@app.get("/user_form/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.post("/user_form/", response_model=schemas.UserInfo)
def create_user_info(request: Request,
                     username: str = Form(...),
                     first_name: str = Form(...),
                     last_name: str = Form(...),
                     phone: str = Form(...),
                     email: str = Form(...),
                     password: str = Form(...),
                     db: Session = Depends(get_db)):
    user_info = schemas.UserInfoCreate(username=username,
                                       first_name=first_name,
                                       last_name=last_name,
                                       phone=phone,
                                       email=email,
                                       password=password)
    db_user_info_username = crud.get_user_info_by_username(db, username=username)
    if db_user_info_username:
        raise HTTPException(status_code=400, detail="Username already saved")
    db_user_info_email = crud.get_user_info_by_email(db, email=email)
    if db_user_info_email:
        raise HTTPException(status_code=400, detail="Email already saved")
    if not phone_validated(phone):
        raise HTTPException(status_code=400, detail="Phone number should be in format +00 123456789 "
                                                    "with a valid country code")
    crud.create_user_info(db=db, user_info=user_info)
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/async_user_form/")
def home_async(request: Request):
    return templates.TemplateResponse("home_async.html", {"request": request})


@app.post("/async_user_form/", response_model=schemas.UserInfo)
def create_user_info_async(request: Request,
                           username: str = Form(...),
                           first_name: str = Form(...),
                           last_name: str = Form(...),
                           phone: str = Form(...),
                           email: str = Form(...),
                           password: str = Form(...)):
    user_info = schemas.UserInfoCreate(username=username,
                                       first_name=first_name,
                                       last_name=last_name,
                                       phone=phone,
                                       email=email,
                                       password=password)
    db_user_info_username = get_user_info_by_username_task.delay(username=username)
    if not db_user_info_username:
        raise HTTPException(status_code=400, detail="Username already saved")
    db_user_info_email = get_user_info_by_email_task.delay(email=email)
    if not db_user_info_email:
        raise HTTPException(status_code=400, detail="Email already saved")
    if not phone_validated_task.delay(phone):
        raise HTTPException(status_code=400, detail="Phone number should be in format +00 123456789 "
                                                    "with a valid country code")
    create_user_info_task.delay(user_info=user_info)
    return templates.TemplateResponse("home.html", {"request": request})
