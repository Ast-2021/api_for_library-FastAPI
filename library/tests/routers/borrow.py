import sys
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from library.main import app
from library.database import Base, get_db
from library.models import Borrow, Books, Authors


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))


SQLALCHEMY_DATABASE_URL = "postgresql://test_user:test_user@localhost/test_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def client():
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client

    with TestingSessionLocal() as session:
        session.query(Borrow).delete()
        session.query(Authors).delete()
        session.query(Books).delete()
        session.commit()


def test_create_borrow(client):
    author_response = client.post("/author/", json={"name": "Test", "last_name": "Author", "date_of_birth": "2000-01-01"})
    author_id = author_response.json()['id']

    book_data = {
        "title": "Test Book",
        "description": "This is a longer description to meet the minimum length requirement for testing purposes.",
        "author_id": author_id,
        "available_quantity": 10
    }

    create_response = client.post("/book/", json=book_data)
    book_id = create_response.json()["id"]

    borrow_data = {
        "book_id": book_id,
        "reader_name": "Test Reader"
    }

    borrow_response = client.post("/borrow/", json=borrow_data)

    assert borrow_response.status_code == 200

    data = borrow_response.json()
    assert data["book_id"] == borrow_data["book_id"]
    assert data["reader_name"] == borrow_data["reader_name"]

    get_book_response = client.get(f"/book/{book_id}")
    book_data = get_book_response.json()
    assert book_data["available_quantity"] == 9


def test_get_borrows(client):
    author_response = client.post("/author/", json={"name": "Test", "last_name": "Author", "date_of_birth": "2000-01-01"})
    author_id = author_response.json()['id']

    book_data = {
        "title": "Test Book",
        "description": "This is a longer description to meet the minimum length requirement for testing purposes.",
        "author_id": author_id,
        "available_quantity": 10
    }

    create_response = client.post("/book/", json=book_data)
    book_id = create_response.json()["id"]

    borrow_data = {
        "book_id": book_id,
        "reader_name": "Test Reader"
    }

    borrow_response = client.post("/borrow/", json=borrow_data)
    borrow_id = borrow_response.json()["id"]

    response = client.get("/borrow/")

    assert response.status_code == 200

    data = response.json()
    assert len(data) > 0
    assert data[0]["book_id"] == borrow_data["book_id"]
    assert data[0]["reader_name"] == borrow_data["reader_name"]


def test_get_borrow(client):
    author_response = client.post("/author/", json={"name": "Test", "last_name": "Author", "date_of_birth": "2000-01-01"})
    author_id = author_response.json()['id']

    book_data = {
        "title": "Test Book",
        "description": "This is a longer description to meet the minimum length requirement for testing purposes.",
        "author_id": author_id,
        "available_quantity": 10
    }

    create_response = client.post("/book/", json=book_data)
    book_id = create_response.json()["id"]

    borrow_data = {
        "book_id": book_id,
        "reader_name": "Test Reader"
    }

    borrow_response = client.post("/borrow/", json=borrow_data)
    borrow_id = borrow_response.json()["id"]

    response = client.get(f"/borrow/{borrow_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["book_id"] == borrow_data["book_id"]
    assert data["reader_name"] == borrow_data["reader_name"]


def test_update_borrow(client):
    author_response = client.post("/author/", json={"name": "Test", "last_name": "Author", "date_of_birth": "2000-01-01"})
    author_id = author_response.json()['id']

    book_data = {
        "title": "Test Book",
        "description": "This is a longer description to meet the minimum length requirement for testing purposes.",
        "author_id": author_id,
        "available_quantity": 10
    }

    create_response = client.post("/book/", json=book_data)
    book_id = create_response.json()["id"]

    borrow_data = {
        "book_id": book_id,
        "reader_name": "Test Reader"
    }

    borrow_response = client.post("/borrow/", json=borrow_data)
    borrow_id = borrow_response.json()["id"]

    updated_borrow_data = {
        "return_date": "2024-12-16"
    }

    response = client.patch(f"/borrow/{borrow_id}", json=updated_borrow_data)

    assert response.status_code == 200
    data = response.json()
    assert data["return_date"] == updated_borrow_data["return_date"]


def test_delete_borrow(client):
    author_response = client.post("/author/", json={"name": "Test", "last_name": "Author", "date_of_birth": "2000-01-01"})
    author_id = author_response.json()['id']

    book_data = {
        "title": "Test Book",
        "description": "This is a longer description to meet the minimum length requirement for testing purposes.",
        "author_id": author_id,
        "available_quantity": 10
    }

    create_response = client.post("/book/", json=book_data)
    book_id = create_response.json()["id"]

    borrow_data = {
        "book_id": book_id,
        "reader_name": "Test Reader"
    }

    borrow_response = client.post("/borrow/", json=borrow_data)
    borrow_id = borrow_response.json()["id"]

    response = client.delete(f"/borrow/{borrow_id}")
    assert response.status_code == 204

    get_response = client.get(f"/borrow/{borrow_id}")
    assert get_response.status_code == 404
