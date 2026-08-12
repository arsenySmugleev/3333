import logging
from uuid import UUID

from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.config import Settings
from src.exceptions.exceptions import NotFoundException
from src.models.appointment import Appointment as AppointmentModel
from src.models.doctor import Doctor as DoctorModel
from src.schemas.doctor import (
    DoctorWithAppointmentCreate,
    DoctorWithAppointmentResponse,
    DoctorWithAppointmentUpdate,
)

logger = logging.getLogger(__name__)
settings = Settings()


class DoctorAppointmentService:

    def __init__(self, session: AsyncSession, redis: Redis):
        self.session = session
        self.redis = redis

    @staticmethod
    def _cache_key(doctor_id: UUID) -> str:
        return f"doctor:{doctor_id}"

    async def _invalidate_cache(self, doctor_id: UUID) -> None:
        await self.redis.delete(self._cache_key(doctor_id))

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
            .execution_options(populate_existing=True)
        )
        doctor = result.scalar_one_or_none()
        if not doctor:
            message = f"Doctor {doctor_id} not found"
            logger.warning(message)
            raise NotFoundException(message)
        return doctor

    async def get_doctor_with_appointment(self, doctor_id: UUID) -> DoctorWithAppointmentResponse:
        cache_key = self._cache_key(doctor_id)
        cached = await self.redis.get(cache_key)
        if cached is not None:
            return DoctorWithAppointmentResponse.model_validate_json(cached)

        doctor = await self._get_doctor_model(doctor_id)
        response = DoctorWithAppointmentResponse.from_model(doctor)
        await self.redis.set(
            cache_key,
            response.model_dump_json(),
            ex=settings.cache_ttl_seconds,
        )
        return response

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
        await self._invalidate_cache(doctor_id)
        doctor = await self._get_doctor_model(doctor_id)
        return DoctorWithAppointmentResponse.from_model(doctor)

    async def delete_doctor_with_appointment(self, doctor_id: UUID) -> None:
        doctor = await self._get_doctor_model(doctor_id)
        doctor.is_deleted = True
        for appointment in doctor.appointment:
            appointment.is_deleted = True
        await self.session.flush()
        await self._invalidate_cache(doctor_id)
