from celery import shared_task
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from . import models, schemas


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_info_by_username(db: Session, username: str):
    return db.query(models.UserInfo).filter(models.UserInfo.email == username).first()


def get_user_info_by_email(db: Session, email: str):
    return db.query(models.UserInfo).filter(models.UserInfo.email == email).first()


def get_password_hash(password):
    return pwd_context.hash(password)


def create_user_info(db: Session, user_info: schemas.UserInfoCreate):
    hashed_password = get_password_hash(user_info.password)
    db_user_info = models.UserInfo(
        username=user_info.username,
        first_name=user_info.first_name,
        last_name=user_info.last_name,
        phone=user_info.phone,
        email=user_info.email,
        hashed_password=hashed_password)
    db.add(db_user_info)
    db.commit()
    db.refresh(db_user_info)
    return db_user_info


@shared_task
def get_user_info_by_username_task(db: Session, username: str):
    return db.query(models.UserInfo).filter(models.UserInfo.email == username).first()


@shared_task
def get_user_info_by_email_task(db: Session, email: str):
    return db.query(models.UserInfo).filter(models.UserInfo.email == email).first()


@shared_task
def get_password_hash_task(password):
    return pwd_context.hash(password)


@shared_task
def create_user_info_task(db: Session, user_info: schemas.UserInfoCreate):
    hashed_password = get_password_hash_task(user_info.password)
    db_user_info = models.UserInfo(
        username=user_info.username,
        first_name=user_info.first_name,
        last_name=user_info.last_name,
        phone=user_info.phone,
        email=user_info.email,
        hashed_password=hashed_password)
    db.add(db_user_info)
    db.commit()
    db.refresh(db_user_info)
    return db_user_info
