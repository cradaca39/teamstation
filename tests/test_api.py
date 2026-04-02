import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_health_returns_200_with_expected_body():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "1.0.0"}


def test_list_items_returns_200_with_list():
    response = client.get("/items")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # Each item has the expected fields
    for item in data:
        assert "id" in item
        assert "name" in item
        assert "price" in item


def test_create_item_returns_201_with_created_item():
    payload = {"name": "Thingamajig", "description": "A thingamajig", "price": 14.99}
    response = client.post("/items", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["description"] == payload["description"]
    assert data["price"] == payload["price"]
    assert "id" in data


def test_create_item_appears_in_list():
    payload = {"name": "Whatchamacallit", "price": 7.50}
    post_response = client.post("/items", json=payload)
    assert post_response.status_code == 201
    new_id = post_response.json()["id"]

    get_response = client.get("/items")
    ids = [item["id"] for item in get_response.json()]
    assert new_id in ids
