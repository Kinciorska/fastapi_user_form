import phonenumbers

from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from config import settings, SQLALCHEMY_DATABASE_URL
from app import models, schemas, database

engine = create_engine(SQLALCHEMY_DATABASE_URL)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

celery_app = Celery(__name__)
celery_app.conf.broker_url = settings.CELERY_BROKER_URL
celery_app.conf.result_backend = settings.CELERY_RESULT_BACKEND
celery_app.conf.event_serializer = 'pickle'
celery_app.conf.task_serializer = 'pickle'
celery_app.conf.result_serializer = 'pickle'
celery_app.conf.accept_content = ['application/json', 'application/x-python-serialize']

celery_app.autodiscover_tasks()

__all__ = 'celery_app'


@celery_app.task(name="create_task")
def create_task():
    return True


@celery_app.task(name="phone_validated_task")
def phone_validated_task(phone_number):
    try:
        parsed_phone_number = phonenumbers.parse(phone_number, None)
        return phonenumbers.is_possible_number(parsed_phone_number)
    except phonenumbers.phonenumberutil.NumberParseException:
        return False


@celery_app.task(name="get_user_info_by_username_task")
def get_user_info_by_username_task(username: str):
    with Session(engine) as session:
        if session.query(models.UserInfo).filter(models.UserInfo.username == username).first():
            return False
        return True


@celery_app.task(name="get_user_info_by_email_task")
def get_user_info_by_email_task(email: str):
    with Session(engine) as session:
        if session.query(models.UserInfo).filter(models.UserInfo.email == email).first():
            return False
        return True


@celery_app.task(name="get_password_hash_task")
def get_password_hash_task(password):
    return {'result': pwd_context.hash(password)}


@celery_app.task(name="create_user_info_task")
def create_user_info_task(user_info: schemas.UserInfoCreate):
    with Session(engine) as session:
        hashed_password = pwd_context.hash(user_info.password)
        db_user_info = models.UserInfo(
            username=user_info.username,
            first_name=user_info.first_name,
            last_name=user_info.last_name,
            phone=user_info.phone,
            email=user_info.email,
            hashed_password=hashed_password)
        session.add(db_user_info)
        session.commit()
        session.refresh(db_user_info)
