import json

import playhouse
import pytest
from flask import url_for

from server.models import User, Tag
from server.utils import createsuperuser


class TestUtils:
    def test_utils_create_superuser(self):
        createsuperuser(email="foo0@bar.org", password="princess123")
        user = User.select().where(User.email == "foo0@bar.org")
        user = user[0]
        assert user.email == "foo0@bar.org"
        assert user.is_admin == True
        with pytest.raises(Exception):
            createsuperuser(email="foo0@bar.org", password="princess123")


class TestAPI:
    def test_login_endpoint(self, client):
        createsuperuser(email="foo1@bar.org", password="princess123")
        res = client.post(
            url_for("login"),
            data=json.dumps(
                {"email": "wronguser@bar.org", "password": "wrong_password"}
            ),
            content_type="application/json",
        )
        assert res.status_code == 401
        res = client.post(
            url_for("login"),
            data=json.dumps({"email": "foo1@bar.org", "password": "wrong_password"}),
            content_type="application/json",
        )
        assert res.status_code == 401
        res = client.post(
            url_for("login"),
            data=json.dumps({"email": "foo1@bar.org", "password": "princess123"}),
            content_type="application/json",
        )
        assert res.status_code == 200

    def test_api_terminals_endpoint(self, client, credentials):
        res = client.post(
            url_for("terminals"),
            headers=credentials,
        )
        assert res.status_code == 201
        registration_token = res.json.get("registration_token")
        res = client.get(url_for("terminals"), headers=credentials)
        assert res.json == [{"id": 1, "registration_token": registration_token}]
        res = client.get(url_for("terminal", registration_token=registration_token))
        assert res.status_code == 200
        res = client.get(url_for("terminal", registration_token="foo"))
        assert res.status_code == 404
        assert res.json == {"error": "404"}

    def test_api_tag_creation(self, client, credentials):
        res = client.post(
            url_for("tags"),
            headers=credentials,
        )
        assert res.status_code == 201
        tag = Tag.get(Tag.id == 1)
        res = client.post(
            url_for("verify_tag"),
            data=json.dumps({"content": "foo"}),
            content_type="application/json",
        )
        assert res.status_code == 401
        res = client.post(
            url_for("verify_tag"),
            data=json.dumps({"content": tag.content}),
            content_type="application/json",
        )
        assert res.status_code == 200
