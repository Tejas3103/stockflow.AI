import pytest
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["Hello"] == "World"
    assert data["status"] == "running"
    assert "timestamp" in data