import sys
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from library.main import app
from library.database import Base, get_db
from library.models import Books, Authors


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
        session.query(Books).delete()
        session.query(Authors).delete()
        session.commit()

    
def test_create_book(client):
    author_response = client.post("/author/", json={"name": "Test", "last_name": "Author", "date_of_birth": "2000-01-01"})
    author_id = author_response.json()['id']

    book_data = {
        "title": "Test Book",
        "description": "This is a longer description to meet the minimum length requirement for testing purposes.",
        "author_id": author_id,
        "available_quantity": 10
    }

    response = client.post("/book/", json=book_data)
    print(response.json())
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == book_data["title"]
    assert data["description"] == book_data["description"]
    assert data["author_id"] == book_data["author_id"]
    assert data["available_quantity"] == book_data["available_quantity"]


def test_get_books(client):
    author_response = client.post("/author/", json={"name": "Test", "last_name": "Author", "date_of_birth": "2000-01-01"})
    author_id = author_response.json()['id']

    book_data = {
        "title": "Test Book",
        "description": "This is a longer description to meet the minimum length requirement for testing purposes.",
        "author_id": author_id,
        "available_quantity": 10
    }

    client.post("/book/", json=book_data)

    response = client.get("/book/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["title"] == book_data["title"]
    assert data[0]["description"] == book_data["description"]
    assert data[0]["author_id"] == book_data["author_id"]
    assert data[0]["available_quantity"] == book_data["available_quantity"]


def test_get_book(client):
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

    response = client.get(f"/book/{book_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == book_data["title"]
    assert data["description"] == book_data["description"]
    assert data["author_id"] == book_data["author_id"]
    assert data["available_quantity"] == book_data["available_quantity"]


def test_update_book(client):
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

    updated_book_data = {
        "title": "Updated Test Book",
        "description": "This is an updated description to meet the minimum length requirement for testing purposes.",
        "author_id": author_id,
    }

    response = client.put(f"/book/{book_id}", json=updated_book_data)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == updated_book_data["title"]
    assert data["description"] == updated_book_data["description"]
    assert data["author_id"] == updated_book_data["author_id"]


def test_delete_book(client):
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

    response = client.delete(f"/book/{book_id}")
    assert response.status_code == 204

    get_response = client.get(f"/book/{book_id}")
    assert get_response.status_code == 404
