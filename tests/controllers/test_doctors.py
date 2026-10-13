from datetime import datetime, timezone
from uuid import uuid4

import pytest
from httpx import AsyncClient


CREATE_PAYLOAD = {
    "name": "House",
    "specialty": "diagnostics",
    "appointment": [
        {
            "time_start": datetime(2026, 8, 10, 10, 0, tzinfo=timezone.utc).isoformat(),
            "name": "checkup",
        }
    ],
}


@pytest.mark.asyncio
async def test_create_and_get_doctor_endpoint(client: AsyncClient):
    create_response = await client.post("/api/v1/doctor_appointment/", json=CREATE_PAYLOAD)
    assert create_response.status_code == 201
    body = create_response.json()
    doctor_id = body["id"]
    assert body["name"] == "House"
    assert len(body["appointment"]) == 1

    get_response = await client.get(f"/api/v1/doctor_appointment/{doctor_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == doctor_id


@pytest.mark.asyncio
async def test_get_doctor_not_found_endpoint(client: AsyncClient):
    response = await client.get(f"/api/v1/doctor_appointment/{uuid4()}")
    assert response.status_code == 404
    body = response.json()
    assert body["error"] == "NOT_FOUND"
    assert "not found" in body["reason"]
    assert "request" in body


@pytest.mark.asyncio
async def test_patch_and_delete_doctor_endpoint(client: AsyncClient):
    create_response = await client.post("/api/v1/doctor_appointment/", json=CREATE_PAYLOAD)
    doctor_id = create_response.json()["id"]

    patch_response = await client.patch(
        f"/api/v1/doctor_appointment/{doctor_id}",
        json={"name": "Wilson"},
    )
    assert patch_response.status_code == 200
    assert patch_response.json()["name"] == "Wilson"

    delete_response = await client.delete(f"/api/v1/doctor_appointment/{doctor_id}")
    assert delete_response.status_code == 204

    get_response = await client.get(f"/api/v1/doctor_appointment/{doctor_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_create_doctor_validation_error(client: AsyncClient):
    response = await client.post(
        "/api/v1/doctor_appointment/",
        json={"name": "", "specialty": "diagnostics", "appointment": []},
    )
    assert response.status_code == 422
