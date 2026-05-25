from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException

from src.models.doctor import Doctor as DoctorModel
from src.models.appointment import Appointment as AppointmentModel
from src.schemas.appointment import AppointmentCreate, AppointmentUpdate
from src.schemas.doctor import DoctorCreate, DoctorUpdate


class DoctorAppointmentCrud:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_doctor_with_appointment(self, doctor_id: int) -> DoctorModel:
        result = await self.session.execute(
            select(DoctorModel).where(DoctorModel.id == doctor_id)
            .options(selectinload(DoctorModel.appointment))
        )
        doctor = result.scalar_one_or_none()
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")
        return doctor

    async def create_doctor_with_appointment(self, doctor_data: DoctorCreate, appointment_data: AppointmentCreate):
        doctor = DoctorModel(**doctor_data.model_dump())
        appointment = AppointmentModel(**appointment_data.model_dump())
        doctor.appointment.append(appointment)
        self.session.add(doctor)
        await self.session.flush()
        await self.session.refresh(doctor, attribute_names=["appointment"])
        return doctor

    async def update_doctor_with_appointment(self,
                                             doctor_id: int,
                                             doctor_data: DoctorUpdate,
                                             appointments_to_add: Optional[List[AppointmentCreate]] = None,
                                             appointments_to_update: Optional[List[AppointmentUpdate]] = None):
        doctor = await self.get_doctor_with_appointment(doctor_id)
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")
        if doctor_data:
            doctor_dict = doctor_data.model_dump(exclude_unset=True)
            for key, value in doctor_dict.items():
                if key != "appointment":
                    setattr(doctor, key, value)

        if appointments_to_add:
            for appointment_data in appointments_to_add:
                new_appointment = AppointmentModel(**appointment_data.model_dump())
                doctor.appointment.append(new_appointment)

        if appointments_to_update:
            for update_data in appointments_to_update:
                appointment_id = update_data.id
                if not appointment_id:
                    raise HTTPException(status_code=404, detail="Appointment not found")
                for appointment in doctor.appointment:
                    if appointment.id == appointment_id:
                        update_dict = update_data.model_dump(exclude_unset=True)
                        for key, value in update_dict.items():
                            if key not in ["id", "doctor_id"]:
                                setattr(appointment, key, value)
                        break

        await self.session.flush()
        await self.session.refresh(doctor, attribute_names=["appointment"])
        return doctor

    async def delete_doctor_with_appointment(self, doctor_id: int) -> None:
        doctor = await self.get_doctor_with_appointment(doctor_id)
        await self.session.delete(doctor)
        await self.session.flush()
        return None
