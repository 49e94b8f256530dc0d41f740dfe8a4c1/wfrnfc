import os

import pytest
from flask_jwt_extended import create_access_token

import server
from server.models import User
from server.utils import create_tables

flask_app = server.app


@pytest.fixture(autouse=True)
def database():
    from server.utils import create_tables

    create_tables()
    yield
    os.unlink("sqlite.db")


@pytest.fixture
def app():
    flask_app.config["BCRYPT_LOG_ROUNDS"] = 4
    flask_app.config["PRESERVE_CONTEXT_ON_EXCEPTION"] = False
    flask_app.config["TESTING"] = True
    flask_app.config["WTF_CSRF_ENABLED"] = False
    create_tables()
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def superuser():
    from server.models import User
    from server.utils import createsuperuser

    createsuperuser(email="foo@bar.org", password="princess123")
    user = User.select().where(User.email == "foo@bar.org")
    user = user[0]

    return user


@pytest.fixture
def credentials(superuser):
    superuser = User.select().where(User.email == "foo@bar.org")
    superuser = superuser[0]
    yield [("Authorization", f"Bearer {create_access_token(identity=superuser.email)}")]
