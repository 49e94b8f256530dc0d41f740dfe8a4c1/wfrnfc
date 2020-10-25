import logging
import os
import random
import string
import sys

import coloredlogs
import pyotp
from dotenv import find_dotenv, load_dotenv
from flask import abort, g, jsonify, request
from flask_api import FlaskAPI, status
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from peewee import BooleanField, CharField, Model, SqliteDatabase, TextField
from playhouse.shortcuts import model_to_dict
from werkzeug.security import check_password_hash

from .models import Tag, Terminal, User, database

logger = logging.getLogger(__name__)
coloredlogs.install(level="DEBUG")


# Flask Setup #
app = FlaskAPI(__name__)
app.config.from_object("server.config.Config")
jwt = JWTManager(app)
# End Flask Setup

# Request Handlers
# These two hooks are provided by flask and we will use them
# to create and tear down a database connection on each request.
@app.before_request
def before_request():
    g.db = database
    g.db.connect(reuse_if_open=True)


@app.after_request
def after_request(response):
    g.db.close()
    return response


# End Request Handlers

# Routes #
# LoginView
@app.route("/api/v1/login", methods=["POST"])
def login():
    email = request.data.get("email")
    password = request.data.get("password")

    user = User.select().where(User.email == email)

    if not user:
        return {"error": "401"}, 401

    user = user[0]

    if not check_password_hash(user.password, password):
        return {"error": "401"}, 401

    return {"access_token": create_access_token(identity=user.email)}


# Terminal Create/ListView
@app.route("/api/v1/terminals", methods=["GET", "POST"])
@jwt_required
def terminals():
    if request.method == "POST":
        registration_token = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=14)
        )
        terminal = Terminal.create(registration_token=registration_token)
        return model_to_dict(terminal), status.HTTP_201_CREATED
    return [model_to_dict(terminal) for terminal in Terminal.select()]


# Terminal DetailView
@app.route("/api/v1/terminals/<registration_token>", methods=["GET"])
def terminal(registration_token):
    try:
        terminal = Terminal.get(Terminal.registration_token == registration_token)
        return model_to_dict(terminal)
    except:
        return {"error": "404"}, 404


# Tag CreateView
@app.route("/api/v1/tags", methods=["POST"])
def tags():
    content = "".join(random.choices(string.ascii_uppercase + string.digits, k=14))
    tag = Tag.create(content=content, tan_secret=pyotp.random_base32())
    return model_to_dict(tag), status.HTTP_201_CREATED


# Tag DetailView
@app.route("/api/v1/tags/verify", methods=["POST"])
def verify_tag():
    content = request.data.get("content")
    try:
        tag = Tag.get(Tag.content == content)
        return {"content": tag.content}
    except:
        return {"error": "401"}, 401


# TAN VerificationView
@app.route("/api/v1/tags/verify/tan", methods=["POST"])
def verify_tan():
    content = request.data.get("content")
    tan_key = request.data.get("tan_key")
    try:
        tag = Tag.get(Tag.content == content)
        totp = pyotp.TOTP(tag.tan_secret)
        logging.debug(f"Retrieved TAN Key {tag.tan_secret}")
        logging.debug(f"Verifying TAN key {tan_key}")
        if totp.verify(tan_key):
            return {}, 200
        else:
            raise Exception()
    except:
        return {"error": "401"}, 401


# End Routes #
