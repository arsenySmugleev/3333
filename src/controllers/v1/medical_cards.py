from uuid import UUID

from fastapi import APIRouter, status

from src.db import get_session
from src.services.med_card_insurance import MedCardInsuranceCrud
from src.schemas.med_card_with_insurance import (
    MedCardInsuranceCreate,
    MedCardInsuranceResponse,
    MedCardInsuranceUpdate,
)

router = APIRouter(prefix="/med_card_insurance", tags=["med_card_with_insurance"])


@router.get("/{med_card_id}", response_model=MedCardInsuranceResponse, status_code=status.HTTP_200_OK)
async def get_med_card_with_insurance(med_card_id: UUID):
    async with get_session() as session:
        crud = MedCardInsuranceCrud(session)
        reed = await crud.get_med_card_with_insurance(med_card_id)
        return reed


@router.post("/", response_model=MedCardInsuranceResponse, status_code=status.HTTP_201_CREATED)
async def create_med_card_with_insurance(med_card_data: MedCardInsuranceCreate):
    async with get_session() as session:
        crud = MedCardInsuranceCrud(session)
        create = await crud.create_med_card_with_insurance(med_card_data)
        return create


@router.patch("/{med_card_id}", response_model=MedCardInsuranceResponse, status_code=status.HTTP_200_OK)
async def update_med_card_with_insurance(
        med_card_id: UUID,
        update_data: MedCardInsuranceUpdate
):
    async with get_session() as session:
        crud = MedCardInsuranceCrud(session)
        update = await crud.update_med_card_with_insurance(
            med_card_id,
            update_data
        )
        return update


@router.delete("/{med_card_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_med_card_with_insurance(med_card_id: UUID):
    async with get_session() as session:
        crud = MedCardInsuranceCrud(session)
        delete = await crud.delete_med_card_with_insurance(med_card_id)
        return delete
