from app.app import app
from app.repository.database import db
from app.repository.user import AppUser
from flask_jwt_extended import decode_token
from app.rbac.rbac import check_password, get_hashed_password, get_token
from datetime import datetime
import pytest


@pytest.fixture
def client():
    app.config["TESTING"] = True

    db.create_all()

    with app.app_context():
        with app.test_client() as client:
            yield client

    db.session.remove()
    db.drop_all()


def test_check_password():
    password = "TestPassword"
    hashed_password = get_hashed_password(password)
    assert check_password(password, hashed_password)


def test_get_token(client):
    timestamp = datetime(2000, 5, 5, 5, 5, 5, 5)
    password = get_hashed_password("TestPassword1")
    user = AppUser(
        id=7,
        timestamp=timestamp,
        username="TestUsername1",
        password=password,
        user_role="user",
        name="TestName1",
        surname="TestSurname1",
        email="TestEmail1",
        phone_number="TestPhoneNumber1",
        website="TestWebsite1",
        agent_request=True,
        banned=False,
        deleted=False,
    )
    token = get_token(user)
    decoded_token = decode_token(token)
    assert "sub" in decoded_token
    assert decoded_token["sub"]["id"] == user.id
    assert decoded_token["sub"]["timestamp"] is not None
    assert decoded_token["sub"]["username"] == user.username
    assert decoded_token["sub"]["user_role"] == user.user_role
    assert decoded_token["sub"]["name"] == user.name
    assert decoded_token["sub"]["surname"] == user.surname
    assert decoded_token["sub"]["email"] == user.email
    assert decoded_token["sub"]["phone_number"] == user.phone_number
    assert decoded_token["sub"]["website"] == user.website
    assert decoded_token["sub"]["agent_request"] == user.agent_request
    assert decoded_token["sub"]["banned"] == user.banned
    assert decoded_token["sub"]["deleted"] == user.deleted
