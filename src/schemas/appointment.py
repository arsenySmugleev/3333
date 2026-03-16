from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

from src.schemas.doctor import Doctor


class AppointmentBase(BaseModel):
    doc_id: int
    time_start: datetime
    name: str


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    doc_id: Optional[int] = None
    time_start: Optional[datetime] = None
    name: Optional[str] = None


class Appointment(AppointmentBase):
    doctor: Optional[Doctor] = None
    model_config = ConfigDict(from_attributes=True, ser_json_bytes='utf8')
