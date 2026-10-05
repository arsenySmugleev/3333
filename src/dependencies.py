from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.cache import RedisCache, get_cache
from src.db import get_session
from src.services.doctor_appointment import DoctorAppointmentService
from src.services.med_card_insurance import MedCardInsuranceService
from src.services.patient_med_service import PatientMedServiceService


def get_doctor_appointment_service(
    session: AsyncSession = Depends(get_session),
    cache: RedisCache = Depends(get_cache),
) -> DoctorAppointmentService:
    return DoctorAppointmentService(session, cache)


def get_patient_med_service_service(
    session: AsyncSession = Depends(get_session),
    cache: RedisCache = Depends(get_cache),
) -> PatientMedServiceService:
    return PatientMedServiceService(session, cache)


def get_med_card_insurance_service(
    session: AsyncSession = Depends(get_session),
    cache: RedisCache = Depends(get_cache),
) -> MedCardInsuranceService:
    return MedCardInsuranceService(session, cache)
