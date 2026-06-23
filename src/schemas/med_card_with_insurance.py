from typing import Optional
from pydantic import BaseModel, ConfigDict

from src.schemas.insurance import Insurance, InsuranceCreate, InsuranceUpdate
from src.schemas.med_card import MedCard, MedCardCreate, MedCardUpdate
from src.models.med_card import MedCard as MedCardModel


class MedCardInsuranceCreate(BaseModel):
    med_card: MedCardCreate
    insurance: InsuranceCreate
    model_config = ConfigDict(from_attributes=True)

    def map_data(self) -> MedCardModel:
        med_card = MedCardModel(**self.med_card.model_dump())
        insurance = self.insurance.map_data()
        med_card.insurance = insurance
        insurance.med_card = med_card
        return med_card


class MedCardInsuranceUpdate(BaseModel):
    med_card: Optional[MedCardUpdate] = None
    insurance: Optional[InsuranceUpdate] = None
    model_config = ConfigDict(from_attributes=True)

    def apply_to(self, med_card: MedCardModel) -> None:
        if self.med_card is not None:
            self.med_card.apply_to(med_card)
        if self.insurance is not None:
            self.insurance.apply_to(med_card.insurance)


class MedCardInsuranceResponse(MedCard):
    insurance: "Insurance"
    model_config = ConfigDict(from_attributes=True)
