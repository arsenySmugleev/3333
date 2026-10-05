from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.dependencies import get_med_card_insurance_service
from src.schemas.med_card import (
    MedCardInsuranceCreate,
    MedCardInsuranceResponse,
    MedCardInsuranceUpdate,
)
from src.services.med_card_insurance import MedCardInsuranceService

router = APIRouter(prefix="/med_card_insurance", tags=["med_card_with_insurance"])


@router.get("/{med_card_id}", response_model=MedCardInsuranceResponse)
async def get_med_card_with_insurance(
    med_card_id: UUID,
    service: MedCardInsuranceService = Depends(get_med_card_insurance_service),
):
    return await service.get_med_card_with_insurance(med_card_id)


@router.post("/", response_model=MedCardInsuranceResponse, status_code=status.HTTP_201_CREATED)
async def create_med_card_with_insurance(
    med_card_data: MedCardInsuranceCreate,
    service: MedCardInsuranceService = Depends(get_med_card_insurance_service),
):
    return await service.create_med_card_with_insurance(med_card_data)


@router.patch("/{med_card_id}", response_model=MedCardInsuranceResponse)
async def update_med_card_with_insurance(
    med_card_id: UUID,
    update_data: MedCardInsuranceUpdate,
    service: MedCardInsuranceService = Depends(get_med_card_insurance_service),
):
    return await service.update_med_card_with_insurance(med_card_id, update_data)


@router.delete("/{med_card_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_med_card_with_insurance(
    med_card_id: UUID,
    service: MedCardInsuranceService = Depends(get_med_card_insurance_service),
):
    await service.delete_med_card_with_insurance(med_card_id)
