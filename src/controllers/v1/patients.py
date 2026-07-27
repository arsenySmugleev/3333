from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_session
from src.schemas.patient import (
    PatientWithMedServiceCreate,
    PatientWithMedServiceResponse,
    PatientWithMedServiceUpdate,
)
from src.services.patient_med_service import PatientMedServiceService

router = APIRouter(prefix="/patient_med_service", tags=["patient_with_med_service"])


@router.get("/{patient_id}", response_model=PatientWithMedServiceResponse)
async def get_patient_with_med_service(
    patient_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    service = PatientMedServiceService(session)
    return await service.get_patient_with_med_service(patient_id)


@router.post("/", response_model=PatientWithMedServiceResponse, status_code=status.HTTP_201_CREATED)
async def create_patient_with_med_service(
    patient_data: PatientWithMedServiceCreate,
    session: AsyncSession = Depends(get_session),
):
    service = PatientMedServiceService(session)
    return await service.create_patient_with_med_service(patient_data)


@router.patch("/{patient_id}", response_model=PatientWithMedServiceResponse)
async def update_patient_with_med_service(
    patient_id: UUID,
    update_data: PatientWithMedServiceUpdate,
    session: AsyncSession = Depends(get_session),
):
    service = PatientMedServiceService(session)
    return await service.update_patient_with_med_service(patient_id, update_data)


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient_or_med_service(
    patient_id: UUID = None,
    med_service_id: UUID = None,
    delete_type: str = "patient",
    session: AsyncSession = Depends(get_session),
):
    service = PatientMedServiceService(session)
    await service.delete_patient_or_med_service(patient_id, med_service_id, delete_type)
