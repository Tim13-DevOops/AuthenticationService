from datetime import datetime
from flask import abort
from app.repository.user import AppUser
from app.repository.database import db
import app.rbac.rbac as rbac


def get_users():
    products = AppUser.query.filter_by(deleted=False).all()
    return products


def username_exists(username):
    return AppUser.query.filter_by(username=username).first() is not None


def register(user_dict):
    """
    Register a new user, or creates a pending agent user request.

    user_dict:
        username: str
        password: str
        user_role: 'user' or 'agent'
    """
    user_dict.pop("id", None)
    password = user_dict.pop("password", None)
    username = user_dict["username"]
    if username_exists(username):
        abort(400, "Username taken")
    # user is always first registered as user role, but can have a request
    # to become an agent
    user = AppUser(
        user_role="user",
        agent_request=False,
        banned=False,
        deleted=False,
        **user_dict,
    )
    user.timestamp = datetime.now()

    password_hash = rbac.get_hashed_password(password)
    user.password = password_hash

    db.session.add(user)
    db.session.commit()
    return user


def login(login_dict):
    """Try to log in the user.

    login_dict:
        username: str
        password: str
    """
    user = AppUser.query.filter_by(username=login_dict["username"]).first()
    if not user:
        abort(400, "Invalid username/password")
    if not rbac.check_password(login_dict["password"], user.password):
        abort(400, "Invalid username/password")

    return rbac.get_token(user)


def update_user(user_dict):
    """Change user data. Can't change username.

    user_dict (only contains fields which should be changed):
        id: int
        password: str
        agent_request: True or False
    """
    user_dict.pop("username", None)
    user_dict.pop("user_role", None)
    # get the user who sent this request
    user_from_token = rbac.get_current_user()
    if not user_from_token.id:
        abort(400, "No user logged in")
    query = AppUser.query.filter_by(id=user_from_token.id)
    user = query.first()
    if user is None:
        abort(404, "AppUser not found")
    if "password" in user_dict:
        user_dict["password"] = rbac.get_hashed_password(user_dict["password"])
    if user_dict.get("agent_request", None) and user.role != "user":
        user_dict["agent_request"] = False

    query.update(user_dict)
    db.session.commit()
    return user


def delete_user():
    user_from_token = rbac.get_current_user()
    if not user_from_token.id:
        abort(400, "No user logged in")
    query = AppUser.query.filter_by(id=user_from_token.id)
    user = query.first()
    if user is None:
        abort(404)
    query.update({"deleted": True})
    db.session.commit()
    return user


def ban_user(user_id):
    query = AppUser.query.filter_by(id=user_id)
    user = query.first()
    if user is None:
        abort(404)
    query.update({"banned": True})
    db.session.commit()
    return user


def resolve_agent_request(user_id, approve):
    """Resolve a request for a user to become an agent.

    Args:
        user_id: int: AppUser's id.
        approve: bool: Whether the request is approved.

    """
    query = AppUser.query.filter_by(id=user_id)
    user = query.first()
    if user is None:
        abort(404, "User not found")
    if not user.agent_request:
        abort(400, "User does not have a pending request to become agent")
    if approve:
        query.update({"user_role": "agent", "agent_request": False})
    else:
        query.update({"user_role": "user", "agent_request": False})
    db.session.commit()
    return user
