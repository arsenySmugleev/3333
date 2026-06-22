from typing import List, Optional

from pydantic import ConfigDict, BaseModel

from src.schemas.common import OptionalNameStr
from src.schemas.appointment import Appointment, AppointmentCreate, AppointmentUpdate
from src.schemas.doctor import Doctor, DoctorBase
from src.models.doctor import Doctor as DoctorModel


class DoctorWithAppointmentResponse(Doctor):
    appointment: List[Appointment]


class DoctorWithAppointmentCreate(DoctorBase):
    appointment: List[AppointmentCreate]
    model_config = ConfigDict(from_attributes=True)

    def map_data(self) -> DoctorModel:
        orm_appointments = AppointmentCreate.map_list(self.appointment)
        doctor_dict = self.model_dump(exclude={"appointment"})
        doctor = DoctorModel(**doctor_dict)
        doctor.appointment = orm_appointments
        return doctor


class DoctorWithAppointmentUpdate(BaseModel):
    name: OptionalNameStr = None
    specialty: OptionalNameStr = None
    appointment_to_add: Optional[List[AppointmentCreate]] = None
    appointment_to_update: Optional[List[AppointmentUpdate]] = None
    model_config = ConfigDict(from_attributes=True)

    def map_doctor_dict(self) -> dict:
        return self.model_dump(exclude_unset=True, exclude={'appointment_to_add', 'appointment_to_update'})

    def map_new_appointments(self) -> List:
        if not self.appointment_to_add:
            return []
        return AppointmentCreate.map_list(self.appointment_to_add)

    def map_appointment_updates(self) -> List:
        if not self.appointment_to_update:
            return []
        return AppointmentUpdate.map_list(self.appointment_to_update)
