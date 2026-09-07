from datetime import datetime, timezone

import pytest

from src.exceptions.exceptions import ValidationException
from src.schemas.appointment import AppointmentUpsert


def test_appointment_upsert_requires_fields_for_create():
    with pytest.raises(ValidationException) as exc_info:
        AppointmentUpsert(id=None, time_start=None, name=None)

    assert "time_start" in exc_info.value.message
    assert "name" in exc_info.value.message


def test_appointment_upsert_create_ok():
    appointment = AppointmentUpsert(
        time_start=datetime(2026, 8, 10, 10, 0, tzinfo=timezone.utc),
        name="checkup",
    )
    assert appointment.id is None
    assert appointment.name == "checkup"
