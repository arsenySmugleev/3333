from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.dependencies import get_doctor_appointment_service
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
    service: DoctorAppointmentService = Depends(get_doctor_appointment_service),
):
    return await service.get_doctor_with_appointment(doctor_id)


@router.post("/", response_model=DoctorWithAppointmentResponse, status_code=status.HTTP_201_CREATED)
async def create_doctor_with_appointments(
    doctor_data: DoctorWithAppointmentCreate,
    service: DoctorAppointmentService = Depends(get_doctor_appointment_service),
):
    return await service.create_doctor_with_appointment(doctor_data=doctor_data)


@router.patch("/{doctor_id}", response_model=DoctorWithAppointmentResponse)
async def update_doctor_with_appointments(
    doctor_id: UUID,
    update_data: DoctorWithAppointmentUpdate,
    service: DoctorAppointmentService = Depends(get_doctor_appointment_service),
):
    return await service.update_doctor_with_appointment(doctor_id, update_data)


@router.delete("/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_doctor_with_appointments(
    doctor_id: UUID,
    service: DoctorAppointmentService = Depends(get_doctor_appointment_service),
):
    await service.delete_doctor_with_appointment(doctor_id)
