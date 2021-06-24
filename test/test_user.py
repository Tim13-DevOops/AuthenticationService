from flask import json
import pytest
from app.app import app
from app.repository.database import db
from app.repository.user import AppUser
from datetime import datetime
from app.rbac.rbac import get_hashed_password


def populate_db():
    timestamp = datetime(2000, 5, 5, 5, 5, 5, 5)
    password = get_hashed_password("TestPassword1")
    user1 = AppUser(
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
    db.session.add(user1)
    user2 = AppUser(
        timestamp=timestamp,
        username="TestUsername2",
        password=password,
        user_role="admin",
        name="TestName2",
        surname="TestSurname2",
        email="TestEmail2",
        phone_number="TestPhoneNumber2",
        website="TestWebsite2",
        agent_request=False,
        banned=False,
        deleted=False,
    )
    db.session.add(user2)
    db.session.commit()


@pytest.fixture
def client():
    app.config["TESTING"] = True

    db.create_all()

    populate_db()

    with app.app_context():
        with app.test_client() as client:
            yield client

    db.session.remove()
    db.drop_all()


def test_get_users_happy(client):
    # first log in as admin
    login_data = {"username": "TestUsername2", "password": "TestPassword1"}
    token = client.post(
        "/login", data=json.dumps(login_data), content_type="application/json"
    ).json
    headers = {"Authorization": f"Bearer {token}"}
    result = client.get("/user", headers=headers)
    assert result.status_code == 200
    assert len(result.json) == 2


def test_create_user_happy(client):
    new_user = {
        "username": "TestUsername3",
        "password": "TestPassword3",
        "user_role": "agent",
        "name": "TestName3",
        "surname": "TestSurname3",
        "email": "TestEmail3",
        "phone_number": "TestPhoneNumber3",
        "website": "TestWebsite3",
        "banned": False,
        "deleted": False,
    }
    result = client.post(
        "/user", data=json.dumps(new_user), content_type="application/json"
    )
    assert result.status_code == 200
    assert result.json["username"] == new_user["username"]
    assert (
        result.json["user_role"] == "user"
    )  # the user is of type user, but there is a request to make him an agent
    assert result.json["name"] == new_user["name"]
    assert result.json["surname"] == new_user["surname"]
    assert result.json["email"] == new_user["email"]
    assert result.json["phone_number"] == new_user["phone_number"]
    assert result.json["website"] == new_user["website"]
    assert result.json["agent_request"]
    assert result.json["banned"] == new_user["banned"]
    assert result.json["deleted"] == new_user["deleted"]


def test_create_user_sad(client):
    # the username TestUsername1 is taken
    new_user = {
        "username": "TestUsername1",
        "password": "TestPassword2",
        "user_role": "user",
        "name": "TestName2",
        "surname": "TestSurname2",
        "email": "TestEmail2",
        "phone_number": "TestPhoneNumber2",
        "website": "TestWebsite2",
        "agent_request": False,
        "banned": False,
        "deleted": False,
    }
    result = client.post(
        "/user", data=json.dumps(new_user), content_type="application/json"
    )
    assert result.status_code == 400


def test_update_user_happy(client):
    # first log in
    login_data = {"username": "TestUsername1", "password": "TestPassword1"}
    token = client.post(
        "/login", data=json.dumps(login_data), content_type="application/json"
    ).json
    headers = {"Authorization": f"Bearer {token}"}
    changed_user = {
        "id": 1,
        "username": "TestUsername1",
        "name": "TestName2",
        "surname": "TestSurname2",
    }
    result = client.put(
        "/user",
        data=json.dumps(changed_user),
        headers=headers,
        content_type="application/json",
    )
    assert result.status_code == 200
    assert result.json["name"] == changed_user["name"]
    assert result.json["surname"] == changed_user["surname"]


def test_update_user_sad(client):
    # try to change user while not logged in, which is forbidden
    changed_user = {
        "name": "ChangedName",
    }
    result = client.put(
        "/user", data=json.dumps(changed_user), content_type="application/json"
    )
    assert result.status_code == 401


def test_login_happy(client):
    login_data = {"username": "TestUsername1", "password": "TestPassword1"}
    result = client.post(
        "/login", data=json.dumps(login_data), content_type="application/json"
    )
    assert result.status_code == 200


def test_login_sad(client):
    login_data = {"username": "TestUsername1", "password": "InvalidPassword"}
    result = client.post(
        "/login",
        data=json.dumps(login_data),
        content_type="application/json",
    )
    assert result.status_code == 400


def test_delete_user_happy(client):
    # first log in
    login_data = {"username": "TestUsername1", "password": "TestPassword1"}
    token = client.post(
        "/login", data=json.dumps(login_data), content_type="application/json"
    ).json
    headers = {"Authorization": f"Bearer {token}"}
    result = client.delete("/user", headers=headers)
    assert result.status_code == 200
    assert result.json["deleted"]


def test_delete_user_sad(client):
    # try to delete without logging in
    result = client.delete("/user")
    assert result.status_code == 401


def test_ban_user_happy(client):
    # first log in as admin
    login_data = {"username": "TestUsername2", "password": "TestPassword1"}
    token = client.post(
        "/login", data=json.dumps(login_data), content_type="application/json"
    ).json
    headers = {"Authorization": f"Bearer {token}"}
    result = client.post("/user/1/ban", headers=headers)
    assert result.status_code == 200
    assert result.json["banned"]


def test_ban_user_sad(client):
    # first log in as admin
    login_data = {"username": "TestUsername2", "password": "TestPassword1"}
    token = client.post(
        "/login", data=json.dumps(login_data), content_type="application/json"
    ).json
    headers = {"Authorization": f"Bearer {token}"}
    # non existant user id
    result = client.post("/user/1389/ban", headers=headers)
    assert result.status_code == 404


def test_resolve_agent_request_happy(client):
    # first log in as admin
    login_data = {"username": "TestUsername2", "password": "TestPassword1"}
    token = client.post(
        "/login", data=json.dumps(login_data), content_type="application/json"
    ).json
    headers = {"Authorization": f"Bearer {token}"}
    approve_dict = {"approve": True}
    result = client.post(
        "/user/1/agent_request",
        data=json.dumps(approve_dict),
        content_type="application/json",
        headers=headers,
    )
    assert result.status_code == 200
    assert result.json["user_role"] == "agent"
    assert not result.json["agent_request"]


def test_resolve_agent_request_sad(client):
    # first log in aas admin
    login_data = {"username": "TestUsername2", "password": "TestPassword1"}
    token = client.post(
        "/login", data=json.dumps(login_data), content_type="application/json"
    ).json
    headers = {"Authorization": f"Bearer {token}"}
    approve_dict = {"approve": True}
    # try to approve a request for a user who doesn't have a pending request
    result = client.post(
        "/user/2/agent_request",
        data=json.dumps(approve_dict),
        content_type="application/json",
        headers=headers,
    )
    assert result.status_code == 400
