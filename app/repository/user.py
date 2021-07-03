from datetime import datetime
from .database import db
from dataclasses import dataclass
from app.rbac import rbac


@dataclass
class AppUser(db.Model):
    id: int
    timestamp: datetime
    username: str
    # password: str #this way it will not show up in the json dict
    user_role: str
    name: str
    surname: str
    email: str
    phone_number: str
    website: str
    agent_request: bool
    banned: bool
    deleted: bool

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    user_role = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    surname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(255))
    website = db.Column(db.String(255))
    agent_request = db.Column(db.Boolean, default=False)
    banned = db.Column(db.Boolean, default=False)
    deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"AppUser {self.username}"


def add_user(user):
    user_exists = AppUser.query.filter_by(username=user.username).first()
    if user_exists:
        return

    password_hash = rbac.get_hashed_password(user.password)
    user.password = password_hash
    db.session.add(user)


def populate_admins():

    users = [
        AppUser(
            username="dusanpanda",
            password="dusanko1",
            user_role="admin",
            timestamp=datetime.now(),
            name="dusan",
            surname="panda",
            email="dusanpanda@gmail.com",
            phone_number="1238021093",
            website="www.dusanpanda@gmail.com",
            agent_request=False,
            banned=False,
            deleted=False
        ),
        AppUser(
            username="banepanda",
            password="banko1",
            user_role="agent",
            timestamp=datetime.now(),
            name="bame",
            surname="panda",
            email="banepanda@gmail.com",
            phone_number="1238021094",
            website="www.banepanda@gmail.com",
            agent_request=False,
            banned=False,
            deleted=False
        ),
        AppUser(
            username="otacpanda",
            password="branko1",
            user_role="agent",
            timestamp=datetime.now(),
            name="otac",
            surname="panda",
            email="otacpanda@gmail.com",
            phone_number="1238021094",
            website="www.baepanda@gmail.com",
            agent_request=False,
            banned=False,
            deleted=False
        ),
        AppUser(
            username="user1panda",
            password="userko1",
            user_role="user",
            timestamp=datetime.now(),
            name="user1",
            surname="panda",
            email="user1panda@gmail.com",
            phone_number="1238021094",
            website="www.user1panda@gmail.com",
            agent_request=False,
            banned=False,
            deleted=False
        ),
        AppUser(
            username="user2panda",
            password="userko1",
            user_role="user",
            timestamp=datetime.now(),
            name="user2",
            surname="panda",
            email="user2panda@gmail.com",
            phone_number="1238021094",
            website="www.user2panda@gmail.com",
            agent_request=False,
            banned=False,
            deleted=False
        ),
        AppUser(
            username="user3panda",
            password="userko1",
            user_role="user",
            timestamp=datetime.now(),
            name="user3",
            surname="panda",
            email="user3panda@gmail.com",
            phone_number="1238021094",
            website="www.user3panda@gmail.com",
            agent_request=False,
            banned=False,
            deleted=False
        ),
        AppUser(
            username="user4panda",
            password="userko1",
            user_role="user",
            timestamp=datetime.now(),
            name="user4",
            surname="panda",
            email="user4panda@gmail.com",
            phone_number="1238021094",
            website="www.user4panda@gmail.com",
            agent_request=False,
            banned=False,
            deleted=False
        ),
        AppUser(
            username="user5panda",
            password="userko1",
            user_role="user",
            timestamp=datetime.now(),
            name="user5",
            surname="panda",
            email="user5panda@gmail.com",
            phone_number="1238021094",
            website="www.user5panda@gmail.com",
            agent_request=False,
            banned=False,
            deleted=False
        ),
    ]

    for user in users:
        add_user(user)
    db.session.commit()

