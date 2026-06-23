from uuid import UUID

from fastapi import APIRouter, status

from src.services.patient_med_service import PatientMedServiceCrud
from src.db import get_session
from src.schemas.patient_with_med_service import (
    PatientWithMedServiceCreate,
    PatientWithMedServiceResponse,
    PatientWithMedServiceUpdate,
)

router = APIRouter(prefix="/patient_med_service", tags=["patient_with_med_service"])


@router.get("/{patient_id}", response_model=PatientWithMedServiceResponse, status_code=status.HTTP_200_OK)
async def get_patient_with_med_service(patient_id: UUID):
    async with get_session() as session:
        crud = PatientMedServiceCrud(session)
        get = await crud.get_patient_with_med_service(patient_id)
        return get


@router.post("/", response_model=PatientWithMedServiceResponse, status_code=status.HTTP_201_CREATED)
async def create_patient_with_med_service(patient_data: PatientWithMedServiceCreate):
    async with get_session() as session:
        crud = PatientMedServiceCrud(session)
        create = await crud.create_patient_with_med_service(patient_data)
        return create


@router.patch("/{patient_id}", response_model=PatientWithMedServiceResponse, status_code=status.HTTP_200_OK)
async def update_patient_with_med_service(
        patient_id: UUID,
        update_data: PatientWithMedServiceUpdate
):
    async with get_session() as session:
        crud = PatientMedServiceCrud(session)
        update = await crud.update_patient_with_med_service(
            patient_id,
            update_data
        )
        return update


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient_or_med_service(
        patient_id: UUID = None,
        med_service_id: UUID = None,
        delete_type: str = "patient"  # "patient", "med_service"
):
    async with get_session() as session:
        crud = PatientMedServiceCrud(session)
        delete = await crud.delete_patient_or_med_service(
            patient_id,
            med_service_id,
            delete_type
        )
        return delete
