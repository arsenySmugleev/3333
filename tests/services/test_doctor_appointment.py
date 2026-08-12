from datetime import datetime, timezone
from uuid import uuid4

import pytest

from src.exceptions.exceptions import NotFoundException
from src.schemas.doctor import DoctorWithAppointmentCreate, DoctorWithAppointmentUpdate
from src.schemas.appointment import AppointmentNestedCreate, AppointmentUpsert
from src.services.doctor_appointment import DoctorAppointmentService


def _create_payload(name: str = "House") -> DoctorWithAppointmentCreate:
    return DoctorWithAppointmentCreate(
        name=name,
        specialty="diagnostics",
        appointment=[
            AppointmentNestedCreate(
                time_start=datetime(2026, 8, 10, 10, 0, tzinfo=timezone.utc),
                name="checkup",
            )
        ],
    )


@pytest.mark.asyncio
async def test_create_and_get_doctor(doctor_service: DoctorAppointmentService):
    created = await doctor_service.create_doctor_with_appointment(_create_payload())

    assert created.name == "House"
    assert created.specialty == "diagnostics"
    assert len(created.appointment) == 1
    assert created.appointment[0].name == "checkup"

    fetched = await doctor_service.get_doctor_with_appointment(created.id)
    assert fetched.id == created.id
    assert fetched.name == created.name


@pytest.mark.asyncio
async def test_get_doctor_not_found(doctor_service: DoctorAppointmentService):
    with pytest.raises(NotFoundException):
        await doctor_service.get_doctor_with_appointment(uuid4())


@pytest.mark.asyncio
async def test_get_doctor_uses_cache(doctor_service: DoctorAppointmentService, redis):
    created = await doctor_service.create_doctor_with_appointment(_create_payload())
    cache_key = doctor_service._cache_key(created.id)

    assert await redis.get(cache_key) is None

    await doctor_service.get_doctor_with_appointment(created.id)
    cached = await redis.get(cache_key)
    assert cached is not None
    assert '"name":"House"' in cached or '"name": "House"' in cached

    await redis.set(cache_key, cached.replace("House", "CachedName"))
    fetched = await doctor_service.get_doctor_with_appointment(created.id)
    assert fetched.name == "CachedName"


@pytest.mark.asyncio
async def test_update_invalidates_cache(doctor_service: DoctorAppointmentService, redis):
    created = await doctor_service.create_doctor_with_appointment(_create_payload())
    await doctor_service.get_doctor_with_appointment(created.id)
    cache_key = doctor_service._cache_key(created.id)
    assert await redis.get(cache_key) is not None

    updated = await doctor_service.update_doctor_with_appointment(
        created.id,
        DoctorWithAppointmentUpdate(name="Wilson"),
    )
    assert updated.name == "Wilson"
    assert await redis.get(cache_key) is None


@pytest.mark.asyncio
async def test_delete_soft_deletes_and_invalidates_cache(
    doctor_service: DoctorAppointmentService,
    redis,
):
    created = await doctor_service.create_doctor_with_appointment(_create_payload())
    await doctor_service.get_doctor_with_appointment(created.id)
    cache_key = doctor_service._cache_key(created.id)

    await doctor_service.delete_doctor_with_appointment(created.id)

    assert await redis.get(cache_key) is None
    with pytest.raises(NotFoundException):
        await doctor_service.get_doctor_with_appointment(created.id)


@pytest.mark.asyncio
async def test_update_adds_appointment(doctor_service: DoctorAppointmentService):
    created = await doctor_service.create_doctor_with_appointment(_create_payload())

    updated = await doctor_service.update_doctor_with_appointment(
        created.id,
        DoctorWithAppointmentUpdate(
            appointment=[
                AppointmentUpsert(
                    time_start=datetime(2026, 8, 11, 12, 0, tzinfo=timezone.utc),
                    name="follow-up",
                )
            ]
        ),
    )

    assert len(updated.appointment) == 2
    names = {item.name for item in updated.appointment}
    assert names == {"checkup", "follow-up"}
