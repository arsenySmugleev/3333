from typing import Optional
from fastapi import APIRouter

from src.db import get_session
from src.crud.med_card_insurance_crud import MedCardInsuranceCrud
from src.schemas.med_card import MedCardCreate, MedCardUpdate
from src.schemas.insurance import InsuranceCreate, InsuranceUpdate
from src.schemas.med_card_with_insurance import MedCardInsuranceResponse

router = APIRouter(prefix="/med_card_insurance", tags=["med_card_with_insurance"])


@router.get("/{id}", response_model=MedCardInsuranceResponse)
async def get_med_card_with_insurance(id: int):
    async with get_session() as session:
        crud = MedCardInsuranceCrud(session)
        reed = await crud.get_med_card_with_insurance(id)
        return reed


@router.post("/", response_model=MedCardInsuranceResponse)
async def create_med_card_with_insurance(
        med_card_data: MedCardCreate,
        insurance_data: InsuranceCreate
):
    async with get_session() as session:
        crud = MedCardInsuranceCrud(session)
        create = await crud.create_med_card_with_insurance(med_card_data, insurance_data)
        return create


@router.patch("/{id}", response_model=MedCardInsuranceResponse)
async def update_med_card_with_insurance(
        med_card_id: int,
        med_card_data: Optional[MedCardUpdate],
        insurance_data: Optional[InsuranceUpdate]
):
    async with get_session() as session:
        crud = MedCardInsuranceCrud(session)
        update = await crud.update_med_card_with_insurance(
            med_card_id,
            med_card_data,
            insurance_data
        )
        return update


@router.delete("/{id}", status_code=204)
async def delete_med_card_with_insurance(med_card_id: int):
    async with get_session() as session:
        crud = MedCardInsuranceCrud(session)
        delete = await crud.delete_med_card_with_insurance(med_card_id)
        return delete
