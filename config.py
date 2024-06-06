import os
import psycopg2

from celery import Celery
from dotenv import load_dotenv
from fastapi import FastAPI

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# Redis settings
REDIS_ENV_DIR = os.path.join(BASE_DIR, 'envs/.redis')

load_dotenv(REDIS_ENV_DIR)

REDIS_PROTOCOL = os.getenv('REDIS_PROTOCOL')
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_DB_NUMBER = os.getenv('REDIS_DB_NUMBER')

CELERY_BROKER_URL = f'{REDIS_PROTOCOL}://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_NUMBER}'
CELERY_RESULT_BACKEND = f'{REDIS_PROTOCOL}://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_NUMBER}'


class Config:
    CELERY_BROKER_URL: str = os.environ.get("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")
    CELERY_RESULT_BACKEND: str = os.environ.get("CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0")


settings = Config()


app = FastAPI()


celery_app = Celery(
    __name__,
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)
celery_app.autodiscover_tasks()


# PostgreSQL config

POSTGRES_ENV_DIR = os.path.join(BASE_DIR, 'envs/.postgres')

load_dotenv(POSTGRES_ENV_DIR)

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE')

SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DATABASE}"
