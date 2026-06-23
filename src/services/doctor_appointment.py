from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.exceptions.exceptions import AppointmentNotFoundException, DoctorNotFoundException
from src.models.doctor import Doctor as DoctorModel
from src.schemas.doctor_with_appoinment import DoctorWithAppointmentCreate, DoctorWithAppointmentUpdate


class DoctorAppointmentCrud:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_doctor_with_appointment(self, doctor_id: UUID) -> DoctorModel:
        result = await self.session.execute(
            select(DoctorModel).where(DoctorModel.id == doctor_id)
            .options(selectinload(DoctorModel.appointment))
        )
        doctor = result.scalar_one_or_none()
        if not doctor:
            raise DoctorNotFoundException(doctor_id)
        return doctor

    async def create_doctor_with_appointment(self, doctor_data: DoctorWithAppointmentCreate):
        doctor = doctor_data.map_data()

        self.session.add(doctor)
        await self.session.flush()
        await self.session.refresh(doctor, attribute_names=["appointment"])
        return doctor

    async def update_doctor_with_appointment(self,
                                             doctor_id: UUID,
                                             update_data: DoctorWithAppointmentUpdate):
        doctor = await self.get_doctor_with_appointment(doctor_id)
        doctor_dict = update_data.map_doctor_dict()
        if doctor_dict:
            for key, value in doctor_dict.items():
                setattr(doctor, key, value)

        new_appointment = update_data.map_new_appointments()
        if new_appointment:
            doctor.appointment.extend(new_appointment)

        appointments_to_update = update_data.map_appointment_updates()
        if appointments_to_update:
            for updates in appointments_to_update:
                appointment_id = updates.id
                if not appointment_id:
                    raise AppointmentNotFoundException()
                for appointment in doctor.appointment:
                    if appointment.id == appointment_id:
                        for key, value in vars(updates).items():
                            if key not in ["id", "doctor_id"]:
                                setattr(appointment, key, value)
                        break

        await self.session.flush()
        await self.session.refresh(doctor, attribute_names=["appointment"])
        return doctor

    async def delete_doctor_with_appointment(self, doctor_id: UUID) -> None:
        doctor = await self.get_doctor_with_appointment(doctor_id)
        await self.session.delete(doctor)
        await self.session.flush()
        return None
