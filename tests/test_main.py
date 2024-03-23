from pydoc import cli
import sys
import os

import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # noqa
from fastapi.testclient import TestClient

from main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def test_user():
    return {"username": "testuser", "password": "testpass"}


def test_login(client, test_user):
    response = client.post("/login", data=test_user)
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token is not None
    return token


def test_read_main():
    print(test_login(client, test_user))
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
