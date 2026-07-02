from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.models.doctor import Doctor as DoctorModel
from src.schemas.appointment import Appointment, AppointmentNestedCreate, AppointmentUpsert
from src.schemas.common import NameStr, OptionalNameStr


class DoctorBase(BaseModel):
    name: NameStr
    specialty: NameStr


class Doctor(DoctorBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)


class DoctorWithAppointmentResponse(Doctor):
    appointment: List[Appointment]

    @classmethod
    def from_model(cls, doctor: DoctorModel) -> "DoctorWithAppointmentResponse":
        return cls.model_validate(doctor)


class DoctorWithAppointmentCreate(DoctorBase):
    appointment: List[AppointmentNestedCreate]
    model_config = ConfigDict(from_attributes=True)

    def map_data(self) -> DoctorModel:
        doctor = DoctorModel(**self.model_dump(exclude={"appointment"}))
        doctor.appointment = AppointmentNestedCreate.to_model_list(self.appointment)
        return doctor


class DoctorWithAppointmentUpdate(BaseModel):
    name: OptionalNameStr = None
    specialty: OptionalNameStr = None
    appointment: Optional[List[AppointmentUpsert]] = None
    model_config = ConfigDict(from_attributes=True)

    def apply_to(self, doctor: DoctorModel) -> None:
        for key, value in self.model_dump(exclude_unset=True, exclude={"appointment"}).items():
            setattr(doctor, key, value)

        if self.appointment is None:
            return

        appointments_by_id = {appointment.id: appointment for appointment in doctor.appointment}
        for item in self.appointment:
            result = item.apply_to(doctor.id, appointments_by_id)
            if item.id is None:
                doctor.appointment.append(result)
