from uuid import uuid4

import pytest
from httpx import AsyncClient

CREATE_PAYLOAD = {
    "name": "Ivan",
    "med_service": [{"service_name": "Therapy"}],
}


@pytest.mark.asyncio
async def test_create_and_get_patient_endpoint(client: AsyncClient):
    create_response = await client.post("/api/v1/patient_med_service/", json=CREATE_PAYLOAD)
    assert create_response.status_code == 201
    body = create_response.json()
    patient_id = body["id"]
    assert body["name"] == "Ivan"
    assert len(body["med_service"]) == 1
    assert body["med_service"][0]["service_name"] == "Therapy"

    get_response = await client.get(f"/api/v1/patient_med_service/{patient_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == patient_id


@pytest.mark.asyncio
async def test_get_patient_not_found_endpoint(client: AsyncClient):
    response = await client.get(f"/api/v1/patient_med_service/{uuid4()}")
    assert response.status_code == 404
    body = response.json()
    assert body["error"] == "NOT_FOUND"
    assert "not found" in body["reason"]
    assert "request" in body


@pytest.mark.asyncio
async def test_patch_and_delete_patient_endpoint(client: AsyncClient):
    create_response = await client.post("/api/v1/patient_med_service/", json=CREATE_PAYLOAD)
    patient_id = create_response.json()["id"]

    patch_response = await client.patch(
        f"/api/v1/patient_med_service/{patient_id}",
        json={"name": "Petr"},
    )
    assert patch_response.status_code == 200
    assert patch_response.json()["name"] == "Petr"

    delete_response = await client.delete(f"/api/v1/patient_med_service/{patient_id}")
    assert delete_response.status_code == 204

    get_response = await client.get(f"/api/v1/patient_med_service/{patient_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_create_patient_validation_error(client: AsyncClient):
    response = await client.post(
        "/api/v1/patient_med_service/",
        json={"name": "", "med_service": []},
    )
    assert response.status_code == 422
