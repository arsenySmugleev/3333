from uuid import uuid4

import pytest

from src.exceptions.exceptions import NotFoundException
from src.schemas.med_service import MedServiceCreate
from src.schemas.patient import (
    PatientWithMedServiceCreate,
    PatientWithMedServiceUpdate,
)
from src.services.patient_med_service import PatientMedServiceService


def _create_payload(
    name: str = "Ivan",
    service_name: str = "Therapy",
) -> PatientWithMedServiceCreate:
    return PatientWithMedServiceCreate(
        name=name,
        med_service=[MedServiceCreate(service_name=service_name)],
    )


@pytest.mark.asyncio
async def test_create_and_get_patient(patient_service: PatientMedServiceService):
    created = await patient_service.create_patient_with_med_service(_create_payload())

    assert created.name == "Ivan"
    assert len(created.med_service) == 1
    assert created.med_service[0].service_name == "Therapy"

    fetched = await patient_service.get_patient_with_med_service(created.id)
    assert fetched.id == created.id
    assert fetched.name == created.name


@pytest.mark.asyncio
async def test_get_patient_not_found(patient_service: PatientMedServiceService):
    with pytest.raises(NotFoundException):
        await patient_service.get_patient_with_med_service(uuid4())


@pytest.mark.asyncio
async def test_get_patient_uses_cache(patient_service: PatientMedServiceService, redis):
    created = await patient_service.create_patient_with_med_service(_create_payload())
    cache_key = patient_service._cache_key(created.id)

    assert await redis.get(cache_key) is None

    await patient_service.get_patient_with_med_service(created.id)
    cached = await redis.get(cache_key)
    assert cached is not None
    assert "Ivan" in cached

    await redis.set(cache_key, cached.replace("Ivan", "CachedName"))
    fetched = await patient_service.get_patient_with_med_service(created.id)
    assert fetched.name == "CachedName"


@pytest.mark.asyncio
async def test_update_invalidates_cache(patient_service: PatientMedServiceService, redis):
    created = await patient_service.create_patient_with_med_service(_create_payload())
    await patient_service.get_patient_with_med_service(created.id)
    cache_key = patient_service._cache_key(created.id)
    assert await redis.get(cache_key) is not None

    updated = await patient_service.update_patient_with_med_service(
        created.id,
        PatientWithMedServiceUpdate(name="Petr"),
    )
    assert updated.name == "Petr"
    assert await redis.get(cache_key) is None


@pytest.mark.asyncio
async def test_delete_patient_soft_deletes_and_invalidates_cache(
    patient_service: PatientMedServiceService,
    redis,
):
    created = await patient_service.create_patient_with_med_service(_create_payload())
    await patient_service.get_patient_with_med_service(created.id)
    cache_key = patient_service._cache_key(created.id)

    await patient_service.delete_patient_or_med_service(
        patient_id=created.id,
        delete_type="patient",
    )

    assert await redis.get(cache_key) is None
    with pytest.raises(NotFoundException):
        await patient_service.get_patient_with_med_service(created.id)


@pytest.mark.asyncio
async def test_update_replaces_med_services(patient_service: PatientMedServiceService):
    first = await patient_service.create_patient_with_med_service(
        _create_payload(name="Ivan", service_name="Therapy"),
    )
    second = await patient_service.create_patient_with_med_service(
        _create_payload(name="Petr", service_name="Surgery"),
    )
    new_service_id = second.med_service[0].id

    updated = await patient_service.update_patient_with_med_service(
        first.id,
        PatientWithMedServiceUpdate(med_service_ids=[new_service_id]),
    )

    assert len(updated.med_service) == 1
    assert updated.med_service[0].id == new_service_id
    assert updated.med_service[0].service_name == "Surgery"


@pytest.mark.asyncio
async def test_delete_med_service_invalidates_patient_cache(
    patient_service: PatientMedServiceService,
    redis,
):
    created = await patient_service.create_patient_with_med_service(_create_payload())
    med_service_id = created.med_service[0].id
    await patient_service.get_patient_with_med_service(created.id)
    cache_key = patient_service._cache_key(created.id)
    assert await redis.get(cache_key) is not None

    await patient_service.delete_patient_or_med_service(
        med_service_id=med_service_id,
        delete_type="med_service",
    )

    assert await redis.get(cache_key) is None
    fetched = await patient_service.get_patient_with_med_service(created.id)
    assert fetched.med_service == []
