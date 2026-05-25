from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class AppointmentBase(BaseModel):
    doc_id: int
    time_start: datetime
    name: str


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    id: int
    doc_id: Optional[int] = None
    time_start: Optional[datetime] = None
    name: Optional[str] = None


class AppointmentUpdateList(BaseModel):
    appointment_to_update: List[AppointmentUpdate]


class Appointment(AppointmentBase):
    model_config = ConfigDict(from_attributes=True, ser_json_bytes='utf8')
