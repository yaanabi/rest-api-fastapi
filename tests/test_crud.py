import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os
from pathlib import Path

from dotenv import load_dotenv, find_dotenv


# Add the root directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from db import get_db
from models import Base, Category, Product
from main import app

load_dotenv(find_dotenv())

DB_URL = os.getenv('DB_TEST_URL')
engine = create_engine(DB_URL)
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def override_get_db():
    try:
        db = TestingSession()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="module")
def setup_category(db_session):
    category = Category(name="test")
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    return category


def test_create_category(db_session):
    category_data = {
        "name": "Test Category"
    }
    response = client.post("/categories/", json=category_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Category"


def test_create_product(db_session, setup_category):
    response = client.post(
        "/products/", json={"name": "test", "description": "test", "price": 1.0, "category_id": setup_category.id})
    assert response.status_code == 201
    assert response.json()["name"] == "test"
    assert response.json()["description"] == "test"
    assert response.json()["price"] == 1.0
    assert response.json()["category_id"] == setup_category.id

def test_get_product(db_session, setup_category):
    product = Product(name="Test Product", price=99.99, category_id=setup_category.id)
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)
    
    response = client.get(f"/products/{product.id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Product"
    assert response.json()["price"] == 99.99
    assert response.json()["category_id"] == setup_category.id

def test_update_product(db_session, setup_category):
    product = Product(name="Test Product", description="Test Description", price=111, category_id=setup_category.id)
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    response = client.patch(f"/products/{product.id}", json={"name": "Updated Name"})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"
    assert response.json()["description"] == "Test Description"
    assert response.json()["price"] == 111
    assert response.json()["category_id"] == setup_category.id

    response = client.patch(f"/products/{product.id}", json={"price": 222})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"
    assert response.json()["description"] == "Test Description"
    assert response.json()["price"] == 222
    assert response.json()["category_id"] == setup_category.id

    response = client.patch(f"/products/{product.id}", json={"description": ""})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"
    assert response.json()["description"] == ""
    assert response.json()["price"] == 222
    assert response.json()["category_id"] == setup_category.id

    category = Category(name="Updated Category")
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    response = client.patch(f"/products/{product.id}", json={"category_id": category.id})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"
    assert response.json()["description"] == ""
    assert response.json()["price"] == 222
    assert response.json()["category_id"] == category.id


def test_get_products(db_session, setup_category):
    response = client.get("/products/")
    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.json()[0]["name"] == "test"
    assert response.json()[0]["description"] == "test"
    assert response.json()[0]["price"] == 1.0
    assert response.json()[0]["category_id"] == setup_category.id

def test_delete_product(db_session, setup_category):
    product = Product(name="Test Product", description="test", price=111, category_id=setup_category.id)
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    response = client.delete(f"/products/{product.id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Product"
    assert response.json()["description"] == "test"
    assert response.json()["price"] == 111
    assert response.json()["category_id"] == setup_category.id

def test_get_products_after_delete(db_session, setup_category):
    response = client.get("/products/")
    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.json()[-1]["name"] == "Updated Name"
    assert response.json()[-1]["description"] == ""
    assert response.json()[-1]["price"] == 222
    assert response.json()[-1]["category_id"] != setup_category.id