from typing import Optional, List
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from src.models.appointment import Appointment as AppointmentModel
from src.schemas.common import NameStr, OptionalNameStr


class AppointmentMapper:
    def map_data(self) -> "AppointmentModel":
        return AppointmentModel(**self.model_dump())

    @classmethod
    def map_list(cls, appointments_data: List["AppointmentMapper"]) -> List["AppointmentModel"]:
        if not appointments_data:
            return []
        return [
            appointment.map_data()
            for appointment in appointments_data
        ]


class AppointmentBase(BaseModel):
    doc_id: UUID
    time_start: datetime
    name: NameStr


class AppointmentCreate(AppointmentBase, AppointmentMapper):
    pass


class AppointmentUpdate(BaseModel, AppointmentMapper):
    id: UUID
    doc_id: Optional[UUID] = None
    time_start: Optional[datetime] = None
    name: OptionalNameStr = None


class Appointment(AppointmentBase):
    model_config = ConfigDict(from_attributes=True, ser_json_bytes='utf8')
