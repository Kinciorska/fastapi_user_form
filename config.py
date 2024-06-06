import os
import psycopg2

from dotenv import load_dotenv


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

POSTGRES_ENV_DIR = os.path.join(BASE_DIR, 'envs/.postgres')

load_dotenv(POSTGRES_ENV_DIR)

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE')


SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DATABASE}"
