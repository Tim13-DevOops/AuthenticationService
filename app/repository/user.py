from datetime import datetime
from .database import db
from dataclasses import dataclass


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
