import pytest

from app import app, state


@pytest.fixture
def client():
    state["healthy"] = True
    app.config["TESTING"] = True
    return app.test_client()


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Auto-Healing" in response.data


def test_health_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


def test_break_makes_health_fail(client):
    assert client.post("/break").status_code == 200
    response = client.get("/health")
    assert response.status_code == 503
    assert response.get_json()["status"] == "unhealthy"
