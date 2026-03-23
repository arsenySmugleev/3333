from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

from src.db import get_session
from src.models.med_card import MedCard as MedCardModel
from src.schemas.med_card import MedCardCreate, MedCardUpdate, MedCard


router = APIRouter(prefix="/med_card", tags=["med_card"])


async def get_db_session() -> AsyncSession:
    async with get_session() as session:
        yield session


@router.get("/{id}", response_model=MedCard)
async def get_med_card(
        id: int,
        session: AsyncSession = Depends(get_db_session)
) -> MedCard:
    stmt = select(MedCardModel).where(MedCardModel.id == id).options(selectinload(MedCardModel.insurance))
    result = await session.execute(stmt)
    med_card = result.scalar_one_or_none()
    if not med_card:
        raise HTTPException(status_code=404, detail="MedCard not found")
    return med_card


@router.post("/", response_model=MedCard)
async def create_med_card(
        med_card_data: MedCardCreate,
        session: AsyncSession = Depends(get_db_session)
):
    med_card_db = MedCardModel(**med_card_data.model_dump())
    session.add(med_card_db)
    await session.commit()
    stmt = (select(MedCardModel).where(MedCardModel.id == med_card_db.id)
            .options(selectinload(MedCardModel.insurance)))
    result = await session.execute(stmt)
    med_card_insurance = result.scalar_one_or_none()
    return med_card_insurance


@router.patch("/{id}", response_model=MedCard)
async def update_med_card(
        id: int,
        med_card_data: MedCardUpdate,
        session: AsyncSession = Depends(get_db_session)
):
    stmt = select(MedCardModel).where(MedCardModel.id == id).options(selectinload(MedCardModel.insurance))
    result = await session.execute(stmt)
    med_card_db = result.scalar_one_or_none()
    if not med_card_db:
        raise HTTPException(status_code=404, detail="MedCard not found")
    updated_med_card_data = med_card_data.model_dump(exclude_unset=True)
    for key, value in updated_med_card_data.items():
        setattr(med_card_db, key, value)
    await session.commit()
    await session.refresh(med_card_db)
    return med_card_db


@router.delete("/{id}", status_code=204)
async def delete_med_card(
        id: int,
        session: AsyncSession = Depends(get_db_session)
):
    result = await session.execute(select(MedCardModel).where(MedCardModel.id == id))
    med_card_db = result.scalar_one_or_none()
    if not med_card_db:
        raise HTTPException(status_code=404, detail="MedCard not found")
    await session.delete(med_card_db)
    await session.commit()
    return None
