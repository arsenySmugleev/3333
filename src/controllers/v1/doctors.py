from uuid import UUID
from fastapi import APIRouter, status

from src.db import get_session
from src.schemas.doctor_with_appoinment import (
    DoctorWithAppointmentCreate,
    DoctorWithAppointmentResponse,
    DoctorWithAppointmentUpdate,
)
from src.services.doctor_appointment import DoctorAppointmentCrud

router = APIRouter(prefix="/doctor_appointment", tags=["doctor_with_appointment"])


@router.get("/{doctor_id}", response_model=DoctorWithAppointmentResponse, status_code=status.HTTP_200_OK)
async def get_doctor_with_appointments(doctor_id: UUID):
    async with get_session() as session:
        crud = DoctorAppointmentCrud(session)
        get = await crud.get_doctor_with_appointment(doctor_id)
        return get


@router.post("/", response_model=DoctorWithAppointmentResponse, status_code=status.HTTP_201_CREATED)
async def create_doctor_with_appointments(doctor_data: DoctorWithAppointmentCreate):
    async with get_session() as session:
        crud = DoctorAppointmentCrud(session)
        create = await crud.create_doctor_with_appointment(
            doctor_data=doctor_data
        )
        return create


@router.patch("/{doctor_id}", response_model=DoctorWithAppointmentResponse, status_code=status.HTTP_200_OK)
async def update_doctor_with_appointments(
        doctor_id: UUID,
        update_data: DoctorWithAppointmentUpdate
):
    async with get_session() as session:
        crud = DoctorAppointmentCrud(session)
        update = await crud.update_doctor_with_appointment(
            doctor_id,
            update_data
        )
        return update


@router.delete("/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_doctor_with_appointments(doctor_id: UUID):
    async with get_session() as session:
        crud = DoctorAppointmentCrud(session)
        delete = await crud.delete_doctor_with_appointment(doctor_id)
        return delete
