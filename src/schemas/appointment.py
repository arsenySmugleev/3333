from datetime import datetime
from typing import List, Optional
from uuid import UUID
import logging

from pydantic import BaseModel, ConfigDict, model_validator

from src.exceptions.exceptions import NotFoundException
from src.models.appointment import Appointment as AppointmentModel
from src.schemas.common import NameStr, OptionalNameStr

logger = logging.getLogger(__name__)


class AppointmentNestedCreate(BaseModel):
    time_start: datetime
    name: NameStr

    def to_model(self) -> AppointmentModel:
        return AppointmentModel(time_start=self.time_start, name=self.name)

    @classmethod
    def to_model_list(cls, appointments: List["AppointmentNestedCreate"]) -> List[AppointmentModel]:
        return [appointment.to_model() for appointment in appointments]


class AppointmentUpsert(BaseModel):
    id: Optional[UUID] = None
    time_start: Optional[datetime] = None
    name: OptionalNameStr = None

    @model_validator(mode="after")
    def validate_create_fields(self) -> "AppointmentUpsert":
        if self.id is None and (self.time_start is None or self.name is None):
            raise ValueError("time_start and name are required when creating an appointment")
        return self

    def apply_to(self, doctor_id: UUID, appointments_by_id: dict[UUID, AppointmentModel]) -> AppointmentModel:
        if self.id is None:
            return AppointmentModel(
                doc_id=doctor_id,
                time_start=self.time_start,
                name=self.name,
            )

        appointment = appointments_by_id.get(self.id)
        if appointment is None:
            message = f"Appointment {self.id} not found for doctor {doctor_id}"
            logger.warning(message)
            raise NotFoundException(message)

        for key, value in self.model_dump(exclude_unset=True, exclude={"id"}).items():
            setattr(appointment, key, value)
        return appointment

class AppointmentBase(BaseModel):
    doc_id: UUID
    time_start: datetime
    name: NameStr


class Appointment(AppointmentBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)
