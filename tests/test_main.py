from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_db_connection():
    # Given, When: Make a request to the ping endpoint
    response = client.get("/ping")

    # Then: Check the response
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] is True
