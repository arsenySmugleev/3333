from uuid import uuid4

import pytest
from httpx import AsyncClient

CREATE_PAYLOAD = {
    "med_card": {
        "patient_name": "Ivan",
        "snils": "10940730177",
    },
    "insurance": {
        "policy_number": 1315,
    },
}


@pytest.mark.asyncio
async def test_create_and_get_med_card_endpoint(client: AsyncClient):
    create_response = await client.post("/api/v1/med_card_insurance/", json=CREATE_PAYLOAD)
    assert create_response.status_code == 201
    body = create_response.json()
    med_card_id = body["id"]
    assert body["patient_name"] == "Ivan"
    assert body["snils"] == "10940730177"
    assert body["insurance"]["policy_number"] == 1315

    get_response = await client.get(f"/api/v1/med_card_insurance/{med_card_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == med_card_id


@pytest.mark.asyncio
async def test_get_med_card_not_found_endpoint(client: AsyncClient):
    response = await client.get(f"/api/v1/med_card_insurance/{uuid4()}")
    assert response.status_code == 404
    body = response.json()
    assert body["error"] == "NOT_FOUND"
    assert "not found" in body["reason"]
    assert "request" in body


@pytest.mark.asyncio
async def test_patch_and_delete_med_card_endpoint(client: AsyncClient):
    create_response = await client.post("/api/v1/med_card_insurance/", json=CREATE_PAYLOAD)
    med_card_id = create_response.json()["id"]

    patch_response = await client.patch(
        f"/api/v1/med_card_insurance/{med_card_id}",
        json={
            "med_card": {"patient_name": "Petr"},
            "insurance": {"policy_number": 9999},
        },
    )
    assert patch_response.status_code == 200
    body = patch_response.json()
    assert body["patient_name"] == "Petr"
    assert body["insurance"]["policy_number"] == 9999

    delete_response = await client.delete(f"/api/v1/med_card_insurance/{med_card_id}")
    assert delete_response.status_code == 204

    get_response = await client.get(f"/api/v1/med_card_insurance/{med_card_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_create_med_card_validation_error(client: AsyncClient):
    response = await client.post(
        "/api/v1/med_card_insurance/",
        json={
            "med_card": {"patient_name": "Ivan", "snils": "123"},
            "insurance": {"policy_number": 1},
        },
    )
    assert response.status_code == 422
