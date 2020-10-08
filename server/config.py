from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    PEEWEE_DATABASE = os.getenv("DATABASE")
    DEBUG = os.getenv("DEBUG")
    FLASK_ENV = os.getenv("FLASK_ENV")
    SECRET_KEY = os.getenv("SECRET_KEY")


class TestConfig(Config):
    PEEWEE_DATABASE = os.getenv("TEST_DATABASE")
    TESTING = True
