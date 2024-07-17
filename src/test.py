import pytest
from starlette.testclient import TestClient
from src.main import app
from src.database import init_db


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


@pytest.fixture(scope="module")
def db_session():
    init_db()


def test_get_weather(client, db_session):
    response = client.get("/weather/Moscow")
    assert response.status_code == 200
    data = response.json()
    assert "weather" in data
    assert isinstance(data["weather"], list)
    assert len(data["weather"]) > 0
    first_weather_entry = data["weather"][0]
    assert "temperature" in first_weather_entry
    assert "time" in first_weather_entry
