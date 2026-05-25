from fastapi import APIRouter

from src.crud.patient_med_servise_crud import PatientMedServiceCrud
from src.schemas.med_service import MedServiceCreate
from src.schemas.patient import PatientCreate
from src.db import get_session
from src.schemas.patient_with_med_service import PatientWithMedServiceResponse

router = APIRouter(prefix="/patient_med_service", tags=["patient_with_med_service"])


@router.get("/{id}", response_model=PatientWithMedServiceResponse)
async def get_patient_with_med_service(id: int):
    async with get_session() as session:
        crud = PatientMedServiceCrud(session)
        get = await crud.get_patient_with_med_service(id)
        return get


@router.post("/", response_model=PatientWithMedServiceResponse)
async def create_patient_with_med_service(
        patient_data: PatientCreate,
        med_service_data: MedServiceCreate,
):
    async with get_session() as session:
        crud = PatientMedServiceCrud(session)
        create = await crud.create_patient_with_med_service(
            patient_data,
            med_service_data
        )
        return create


@router.patch("/{id}", response_model=PatientWithMedServiceResponse)
async def update_patient_with_med_service(
        patient_id: int,
        med_service_ids: list[int]
):
    async with get_session() as session:
        crud = PatientMedServiceCrud(session)
        update = await crud.update_patient_with_med_service(
            patient_id,
            med_service_ids
        )
        return update


@router.delete("/{id}", status_code=204)
async def delete_patient_or_med_service(
        patient_id: int = None,
        med_service_id: int = None,
        delete_type: str = "patient",  # "patient", "med_service"
):
    async with get_session() as session:
        crud = PatientMedServiceCrud(session)
        delete = await crud.delete_patient_or_med_service(
            patient_id,
            med_service_id,
            delete_type
        )
        return delete
