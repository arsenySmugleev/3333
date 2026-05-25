from typing import List, Optional
from fastapi import APIRouter

from src.db import get_session
from src.schemas.appointment import AppointmentCreate, AppointmentUpdate
from src.schemas.doctor import DoctorCreate, DoctorUpdate
from src.schemas.doctor_with_appoinment import DoctorWithAppointmentResponse
from src.crud.doctor_appointment_crud import DoctorAppointmentCrud

router = APIRouter(prefix="/doctor_appointment", tags=["doctor_with_appointment"])


@router.get("/{id}", response_model=DoctorWithAppointmentResponse)
async def get_doctor_with_appointments(id: int):
    async with get_session() as session:
        crud = DoctorAppointmentCrud(session)
        get = await crud.get_doctor_with_appointment(id)
        return get


@router.post("/", response_model=DoctorWithAppointmentResponse)
async def create_doctor_with_appointments(
        doctor_data: DoctorCreate,
        appointment_data: AppointmentCreate
):
    async with get_session() as session:
        crud = DoctorAppointmentCrud(session)
        create = await crud.create_doctor_with_appointment(
            doctor_data=doctor_data,
            appointment_data=appointment_data
        )
        return create


@router.patch("/{id}", response_model=DoctorWithAppointmentResponse)
async def update_doctor_with_appointments(
        doctor_id: int,
        doctor_data: DoctorUpdate,
        appointments_to_add: Optional[List[AppointmentCreate]] = None,
        appointments_to_update: Optional[List[AppointmentUpdate]] = None,
):
    async with get_session() as session:
        crud = DoctorAppointmentCrud(session)
        update = await crud.update_doctor_with_appointment(
            doctor_id,
            doctor_data,
            appointments_to_add,
            appointments_to_update
        )
        return update


@router.delete("/{id}", status_code=204)
async def delete_doctor_with_appointments(id: int):
    async with get_session() as session:
        crud = DoctorAppointmentCrud(session)
        delete = await crud.delete_doctor_with_appointment(id)
        return delete
