from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    DEBUG = os.getenv("DEBUG")
    FLASK_ENV = os.getenv("FLASK_ENV")
    SECRET_KEY = os.getenv("SECRET_KEY")


class TestConfig(Config):
    TESTING = True
