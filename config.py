import os

from dotenv import load_dotenv
from fastapi import FastAPI

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# RabbitMQ settings

RABBITMQ_ENV_DIR = os.path.join(BASE_DIR, 'envs/.rabbitmq')

load_dotenv(RABBITMQ_ENV_DIR)

PROTOCOL = os.getenv('RABBITMQ_PROTOCOL')
USER = os.getenv('RABBITMQ_USER')
PASSWORD = os.getenv('RABBITMQ_PASSWORD')
HOST = os.getenv('RABBITMQ_HOST')
PORT = os.getenv('RABBITMQ_PORT')
VHOST = os.getenv('RABBITMQ_DEFAULT_VHOST')


# Celery settings

CELERY_BROKER_URL = f"{PROTOCOL}://{USER}:{PASSWORD}@{HOST}:{PORT}"
CELERY_BACKEND_URL = "rpc://"


class Config:
    CELERY_BROKER_URL: str = CELERY_BROKER_URL
    CELERY_RESULT_BACKEND: str = CELERY_BACKEND_URL


settings = Config()

app = FastAPI()


# PostgreSQL config

POSTGRES_ENV_DIR = os.path.join(BASE_DIR, 'envs/.postgres')

load_dotenv(POSTGRES_ENV_DIR)

POSTGRES_USER = os.getenv('POSTGRES_NON_ROOT_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_NON_ROOT_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')

SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
