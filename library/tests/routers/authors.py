import sys
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from library.main import app
from library.database import Base, get_db
from library.models.authors import Authors


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
        session.query(Authors).delete()
        session.commit()


def test_create_author(client):
    response = client.post("/author/", json={"name": "Test", 
                                             "last_name": "Author", 
                                             "date_of_birth": "2000-01-01"})
    assert response.status_code == 200, response.json()
    data = response.json()
    print(data)
    db = TestingSessionLocal() 
    author = db.query(Authors).filter(Authors.id == data["id"]).first() 
    print(author)
    assert author is not None 
    assert author.name == "Test" 
    assert author.last_name == "Author" 
    assert author.date_of_birth.strftime('%Y-%m-%d') == "2000-01-01" 
    db.close()


def test_get_authors(client):
    client.post("/author/", json={
        "name": "Test1",
        "last_name": "Author1",
        "date_of_birth": "2000-01-01"
    })
    client.post("/author/", json={
        "name": "Test2",
        "last_name": "Author2",
        "date_of_birth": "2000-01-01"
    })

    response = client.get("/author/")
    assert response.status_code == 200, response.json()
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Test1"
    assert data[1]["name"] == "Test2"


def test_get_author(client):
    response_create = client.post("/author/", json={
        "name": "Test",
        "last_name": "Author",
        "date_of_birth": "2000-01-01"
    })
    assert response_create.status_code == 200, response_create.json()
    author_id = response_create.json()["id"]

    response_get = client.get(f"/author/{author_id}")
    assert response_get.status_code == 200, response_get.json()
    data = response_get.json()
    assert data["id"] == author_id
    assert data["name"] == "Test"
    assert data["last_name"] == "Author"
    assert data["date_of_birth"] == "2000-01-01"


def test_update_author(client):
    response_create = client.post("/author/", json={
        "name": "Test",
        "last_name": "Author",
        "date_of_birth": "2000-01-01"
    })
    assert response_create.status_code == 200, response_create.json()
    author_id = response_create.json()["id"]

    response_update = client.put(f"/author/{author_id}", json={
        "name": "UpdatedTest",
        "last_name": "UpdatedAuthor",
        "date_of_birth": "2000-01-01"
    })
    assert response_update.status_code == 200, response_update.json()
    data = response_update.json()
    assert data["name"] == "UpdatedTest"
    assert data["last_name"] == "UpdatedAuthor"
    assert data["date_of_birth"] == "2000-01-01"


def test_delete_author(client):
    response_create = client.post("/author/", json={
        "name": "Test",
        "last_name": "Author",
        "date_of_birth": "2000-01-01"
    })
    assert response_create.status_code == 200, response_create.json()
    author_id = response_create.json()["id"]

    response_delete = client.delete(f"/author/{author_id}")
    assert response_delete.status_code == 204
    
    response_get = client.get(f"/author/{author_id}")
    assert response_get.status_code == 404