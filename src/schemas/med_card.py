from __future__ import annotations

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.models.med_card import MedCard as MedCardModel
from src.schemas.common import NameStr, OptionalNameStr, OptionalSnils, Snils
from src.schemas.insurance import Insurance, InsuranceCreate, InsuranceUpdate


class MedCardBase(BaseModel):
    patient_name: NameStr
    snils: Snils


class MedCardCreate(MedCardBase):
    pass


class MedCardUpdate(BaseModel):
    patient_name: OptionalNameStr = None
    snils: OptionalSnils = None

    def map_dict(self) -> dict:
        return self.model_dump(exclude_unset=True)

    def apply_to(self, med_card: MedCardModel) -> None:
        for key, value in self.map_dict().items():
            setattr(med_card, key, value)


class MedCard(MedCardBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)


class MedCardInsuranceResponse(MedCard):
    insurance: Insurance
    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_model(cls, med_card: MedCardModel) -> "MedCardInsuranceResponse":
        return cls.model_validate(med_card)


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
