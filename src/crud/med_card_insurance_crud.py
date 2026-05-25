from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import Optional
from fastapi import HTTPException

from src.models.med_card import MedCard as MedCardModel
from src.models.insurance import Insurance as InsuranceModel
from src.schemas.insurance import InsuranceCreate, InsuranceUpdate
from src.schemas.med_card import MedCardCreate, MedCardUpdate


class MedCardInsuranceCrud:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_med_card_with_insurance(self, med_card_id: int) -> MedCardModel:
        result = await self.session.execute(select(MedCardModel).where(MedCardModel.id == med_card_id).
                                            options(selectinload(MedCardModel.insurance)))
        med_card = result.scalar_one_or_none()
        if not med_card:
            raise HTTPException(status_code=404, detail="MedCard not found")
        return med_card

    async def create_med_card_with_insurance(self,
                                             med_card_data: MedCardCreate,
                                             insurance_data: InsuranceCreate):
        med_card = MedCardModel(**med_card_data.model_dump())
        insurance = InsuranceModel(**insurance_data.model_dump())
        med_card.insurance = insurance
        insurance.med_card = med_card
        self.session.add(med_card)
        await self.session.flush()
        await self.session.refresh(med_card, attribute_names=["insurance"])
        return med_card

    async def update_med_card_with_insurance(self,
                                             med_card_id: int,
                                             med_card_data: Optional[MedCardUpdate],
                                             insurance_data: Optional[InsuranceUpdate]):
        med_card = await self.get_med_card_with_insurance(med_card_id)
        if not med_card:
            raise HTTPException(status_code=404, detail="MedCard not found")
        if med_card_data:
            update_med_card_data = med_card_data.model_dump(exclude_unset=True)
            for key, value in update_med_card_data.items():
                if hasattr(med_card, key):
                    setattr(med_card, key, value)
        if insurance_data:
            update_insurance_data = insurance_data.model_dump(exclude_unset=True)
            for key, value in update_insurance_data.items():
                if hasattr(med_card.insurance, key):
                    setattr(med_card.insurance, key, value)
                else:
                    raise HTTPException(status_code=404, detail="Insurance not found")
        await self.session.flush()
        await self.session.refresh(med_card, attribute_names=["insurance"])
        return med_card

    async def delete_med_card_with_insurance(self, med_card_id: int) -> None:
        med_card = await self.get_med_card_with_insurance(med_card_id)
        await self.session.delete(med_card)
        await self.session.flush()
        return None
