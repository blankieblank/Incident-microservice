import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_create_incident(client: AsyncClient):
    response = await client.post("/incidents/", json={"description": "Test incident", "source": "monitoring"})
    assert response.status_code == 201
    data = response.json()
    assert data["description"] == "Test incident"
    assert data["source"] == "monitoring"
    assert "id" in data


async def test_update_incident_status(client: AsyncClient):
    response = await client.post("/incidents/", json={"description": "To be updated", "source": "operator"})
    incident_id = response.json()["id"]

    update_response = await client.patch(f"/incidents/{incident_id}", json={"status": "in_progress"})
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["status"] == "in_progress"
    assert data["id"] == incident_id


async def test_update_nonexistent_incident_returns_404(client: AsyncClient):
    response = await client.patch("/incidents/999", json={"status": "closed"})
    assert response.status_code == 404


async def test_get_incidents_happy_path(client: AsyncClient):
    await client.post("/incidents/", json={"description": "First incident", "source": "operator"})
    response = await client.get("/incidents/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1


async def test_get_incidents_with_status_filter_happy_path(client: AsyncClient):
    await client.post("/incidents/", json={"description": "Open one", "source": "partner"})
    response = await client.get("/incidents/?filter_status=open")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["status"] == "open"


async def test_get_incidents_returns_404_on_empty_db(client: AsyncClient):
    response = await client.get("/incidents/")
    assert response.status_code == 404


async def test_get_incidents_returns_404_for_unmatched_filter(client: AsyncClient):
    await client.post("/incidents/", json={"description": "An open incident", "source": "operator"})
    response = await client.get("/incidents/?filter_status=closed")
    assert response.status_code == 404
