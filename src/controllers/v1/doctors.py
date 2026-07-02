from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_session
from src.schemas.doctor import (
    DoctorWithAppointmentCreate,
    DoctorWithAppointmentResponse,
    DoctorWithAppointmentUpdate,
)
from src.services.doctor_appointment import DoctorAppointmentService

router = APIRouter(prefix="/doctor_appointment", tags=["doctor_with_appointment"])


@router.get("/{doctor_id}", response_model=DoctorWithAppointmentResponse)
async def get_doctor_with_appointments(
    doctor_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    service = DoctorAppointmentService(session)
    return await service.get_doctor_with_appointment(doctor_id)


@router.post("/", response_model=DoctorWithAppointmentResponse, status_code=status.HTTP_201_CREATED)
async def create_doctor_with_appointments(
    doctor_data: DoctorWithAppointmentCreate,
    session: AsyncSession = Depends(get_session),
):
    service = DoctorAppointmentService(session)
    return await service.create_doctor_with_appointment(doctor_data=doctor_data)


@router.patch("/{doctor_id}", response_model=DoctorWithAppointmentResponse)
async def update_doctor_with_appointments(
    doctor_id: UUID,
    update_data: DoctorWithAppointmentUpdate,
    session: AsyncSession = Depends(get_session),
):
    service = DoctorAppointmentService(session)
    return await service.update_doctor_with_appointment(doctor_id, update_data)


@router.delete("/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_doctor_with_appointments(
    doctor_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    service = DoctorAppointmentService(session)
    await service.delete_doctor_with_appointment(doctor_id)
