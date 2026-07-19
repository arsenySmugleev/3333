from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.models.doctor import Doctor as DoctorModel
from src.schemas.appointment import Appointment, AppointmentNestedCreate, AppointmentUpsert
from src.schemas.common import NameStr, OptionalNameStr


class DoctorBase(BaseModel):
    name: NameStr
    specialty: NameStr


class DoctorCreate(DoctorBase):
    def map_data(self) -> DoctorModel:
        return DoctorModel(**self.model_dump())


class Doctor(DoctorBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)


class DoctorWithAppointmentResponse(Doctor):
    appointment: List[Appointment]

    @classmethod
    def from_model(cls, doctor: DoctorModel) -> "DoctorWithAppointmentResponse":
        return cls.model_validate(doctor)


class DoctorWithAppointmentCreate(DoctorCreate):
    appointment: List[AppointmentNestedCreate]
    model_config = ConfigDict(from_attributes=True)

    def map_data(self) -> DoctorModel:
        doctor = DoctorCreate.model_validate(self).map_data()
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
