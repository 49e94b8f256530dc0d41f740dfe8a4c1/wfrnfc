from flask import url_for


def test_api_ping(client):
    res = client.get(url_for("hello_world"))
    assert res.json == {"ping": "pong"}
