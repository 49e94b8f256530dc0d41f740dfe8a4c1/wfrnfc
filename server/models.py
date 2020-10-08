import os
import sys

from dotenv import find_dotenv, load_dotenv
from peewee import BooleanField, CharField, Model, SqliteDatabase, TextField

load_dotenv()
if "pytest" in sys.modules:
    PEEWEE_DATABASE = os.getenv("TEST_DATABASE")
else:  # pragma no cover
    PEEWEE_DATABASE = os.getenv("DATABASE")


database = SqliteDatabase(PEEWEE_DATABASE)


class BaseModel(Model):
    class Meta:
        database = database


class User(BaseModel):
    email = CharField(max_length=255, unique=True)
    password = TextField()
    is_admin = BooleanField()


class Terminal(BaseModel):
    registration_token = CharField(max_length=255)


class Object(BaseModel):
    pass


class Tag(BaseModel):
    pass
