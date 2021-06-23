import pytest
from app.app import app
from app.repository.database import db


def populate_db():
    pass


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


def test_example(client):
    assert True
