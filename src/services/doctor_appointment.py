from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.exceptions.exceptions import raise_not_found
from src.models.doctor import Doctor as DoctorModel
from src.schemas.doctor import (
    DoctorWithAppointmentCreate,
    DoctorWithAppointmentResponse,
    DoctorWithAppointmentUpdate,
)


class DoctorAppointmentService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def _get_doctor_model(self, doctor_id: UUID) -> DoctorModel:
        result = await self.session.execute(
            select(DoctorModel).where(DoctorModel.id == doctor_id)
            .options(selectinload(DoctorModel.appointment))
        )
        doctor = result.scalar_one_or_none()
        if not doctor:
            raise_not_found(f"Doctor {doctor_id} not found")
        return doctor

    async def get_doctor_with_appointment(self, doctor_id: UUID) -> DoctorWithAppointmentResponse:
        doctor = await self._get_doctor_model(doctor_id)
        return DoctorWithAppointmentResponse.from_model(doctor)

    async def create_doctor_with_appointment(
        self,
        doctor_data: DoctorWithAppointmentCreate,
    ) -> DoctorWithAppointmentResponse:
        doctor = doctor_data.map_data()

        self.session.add(doctor)
        await self.session.flush()
        await self.session.refresh(doctor, attribute_names=["appointment"])
        return DoctorWithAppointmentResponse.from_model(doctor)

    async def update_doctor_with_appointment(
        self,
        doctor_id: UUID,
        update_data: DoctorWithAppointmentUpdate,
    ) -> DoctorWithAppointmentResponse:
        doctor = await self._get_doctor_model(doctor_id)
        update_data.apply_to(doctor)
        await self.session.flush()
        await self.session.refresh(doctor, attribute_names=["appointment"])
        return DoctorWithAppointmentResponse.from_model(doctor)

    async def delete_doctor_with_appointment(self, doctor_id: UUID) -> None:
        doctor = await self._get_doctor_model(doctor_id)
        await self.session.delete(doctor)
        await self.session.flush()
