from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.exceptions.exceptions import MedCardNotFoundException
from src.models.med_card import MedCard as MedCardModel
from src.schemas.med_card_with_insurance import MedCardInsuranceCreate, MedCardInsuranceUpdate


class MedCardInsuranceCrud:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_med_card_with_insurance(self, med_card_id: UUID) -> MedCardModel:
        result = await self.session.execute(select(MedCardModel).where(MedCardModel.id == med_card_id).
                                            options(selectinload(MedCardModel.insurance)))
        med_card = result.scalar_one_or_none()
        if not med_card:
            raise MedCardNotFoundException(med_card_id)
        return med_card

    async def create_med_card_with_insurance(self, med_card_data: MedCardInsuranceCreate):
        med_card = med_card_data.map_data()
        self.session.add(med_card)
        await self.session.flush()
        await self.session.refresh(med_card, attribute_names=["insurance"])
        return med_card

    async def update_med_card_with_insurance(self,
                                             med_card_id: UUID,
                                             update_data: MedCardInsuranceUpdate):
        med_card = await self.get_med_card_with_insurance(med_card_id)
        update_data.apply_to(med_card)
        await self.session.flush()
        await self.session.refresh(med_card, attribute_names=["insurance"])
        return med_card

    async def delete_med_card_with_insurance(self, med_card_id: UUID) -> None:
        med_card = await self.get_med_card_with_insurance(med_card_id)
        await self.session.delete(med_card)
        await self.session.flush()
        return None
