import os

from dotenv import find_dotenv, load_dotenv

from flask import g
from flask_api import FlaskAPI
from peewee import Model, SqliteDatabase

# Load environment variables
load_dotenv()
PEEWEE_DATABASE = os.getenv("PEEWEE_DATABASE")
DEBUG = os.getenv("DEBUG")
FLASK_ENV = os.getenv("FLASK_ENV")
SECRET_KEY = os.getenv("SECRET_KEY")
# End load environment variables

app = FlaskAPI(__name__)
app.config.from_object(__name__)

database = SqliteDatabase(PEEWEE_DATABASE)

# Request Handlers
# These two hooks are provided by flask and we will use them
# to create and tear down a database connection on each request.
@app.before_request
def before_request():
    g.db = database
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


# End Request Handlers

# Models
class BaseModel(Model):
    class Meta:
        database = database


class Terminal(BaseModel):
    pass


class Object(BaseModel):
    pass


class Tag(BaseModel):
    pass


# End Models

# Utilities #
def create_tables() -> None:
    with database:
        database.create_tables([Object, Tag])


# End Utilites #

# Routes #
@app.route("/", methods=["GET", "POST"])
def hello_world():
    return {"hello": "world"}


# End Routes #

if __name__ == "__main__":
    create_tables()
    app.run()
