import logging
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.exceptions.exceptions import NotFoundException
from src.models.appointment import Appointment as AppointmentModel
from src.models.doctor import Doctor as DoctorModel
from src.schemas.doctor import (
    DoctorWithAppointmentCreate,
    DoctorWithAppointmentResponse,
    DoctorWithAppointmentUpdate,
)

logger = logging.getLogger(__name__)


class DoctorAppointmentService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def _get_doctor_model(self, doctor_id: UUID) -> DoctorModel:
        result = await self.session.execute(
            select(DoctorModel)
            .where(
                DoctorModel.id == doctor_id,
                DoctorModel.is_deleted.is_(False),
            )
            .options(
                selectinload(
                    DoctorModel.appointment.and_(AppointmentModel.is_deleted.is_(False))
                )
            )
        )
        doctor = result.scalar_one_or_none()
        if not doctor:
            message = f"Doctor {doctor_id} not found"
            logger.warning(message)
            raise NotFoundException(message)
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
        doctor = await self._get_doctor_model(doctor.id)
        return DoctorWithAppointmentResponse.from_model(doctor)

    async def update_doctor_with_appointment(
        self,
        doctor_id: UUID,
        update_data: DoctorWithAppointmentUpdate,
    ) -> DoctorWithAppointmentResponse:
        doctor = await self._get_doctor_model(doctor_id)
        new_appointments = update_data.apply_to(doctor)
        if new_appointments:
            self.session.add_all(new_appointments)
        await self.session.flush()
        doctor = await self._get_doctor_model(doctor_id)
        return DoctorWithAppointmentResponse.from_model(doctor)

    async def delete_doctor_with_appointment(self, doctor_id: UUID) -> None:
        doctor = await self._get_doctor_model(doctor_id)
        doctor.is_deleted = True
        for appointment in doctor.appointment:
            appointment.is_deleted = True
        await self.session.flush()
