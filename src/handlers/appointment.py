from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

from src.db import get_session
from src.schemas.appointment import Appointment, AppointmentCreate, AppointmentUpdate
from src.models.appointment import Appointment as AppointmentModel


router = APIRouter(prefix="/appointment", tags=["appointment"])


async def get_db_session() -> AsyncSession:
    async with get_session() as session:
        yield session


@router.get("/{id}", response_model=Appointment)
async def get_appointment(
        id: int,
        session: AsyncSession = Depends(get_db_session)
) -> Appointment:
    stmt = select(AppointmentModel).where(AppointmentModel.id == id).options(selectinload(AppointmentModel.doctor))
    result = await (session.execute(stmt))
    appointment = result.scalar_one_or_none()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment


@router.post("/", response_model=Appointment)
async def create_appointment(
        appointment_data: AppointmentCreate,
        session: AsyncSession = Depends(get_db_session)
):
    appointment_db = AppointmentModel(**appointment_data.model_dump())
    session.add(appointment_db)
    await session.commit()
    stmt = (select(AppointmentModel).where(AppointmentModel.id == appointment_db.id)
            .options(selectinload(AppointmentModel.doctor)))
    result = await session.execute(stmt)
    appointment_db = result.scalar_one_or_none()
    return appointment_db


@router.patch("/{id}", response_model=Appointment)
async def update_appointment(
        id: int,
        appointment_data: AppointmentUpdate,
        session: AsyncSession = Depends(get_db_session)
):
    stmt = (select(AppointmentModel).where(AppointmentModel.id == id)
            .options(selectinload(AppointmentModel.doctor)))
    result = await session.execute(stmt)
    appointment_db = result.scalar_one_or_none()
    if not appointment_db:
        raise HTTPException(status_code=404, detail="Appointment not found")
    update_appointment_data = appointment_data.model_dump(exclude_unset=True)
    for key, value in update_appointment_data.items():
        setattr(appointment_db, key, value)
    await session.commit()
    await session.refresh(appointment_db)
    return appointment_db


@router.delete("/{id}", status_code=204)
async def delete_appointment(
        id: int,
        session: AsyncSession = Depends(get_db_session)
):
    result = await session.execute(select(AppointmentModel).where(AppointmentModel.id == id))
    appointment_db = result.scalar_one_or_none()
    if not appointment_db:
        raise HTTPException(status_code=404, detail="Appointment not found")
    await session.delete(appointment_db)
    await session.commit()
    return None
