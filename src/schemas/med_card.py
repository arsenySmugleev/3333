from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.schemas.common import NameStr, OptionalNameStr

if TYPE_CHECKING:
    from src.models.med_card import MedCard as MedCardModel


class MedCardBase(BaseModel):
    patient_name: NameStr


class MedCardCreate(MedCardBase):
    pass


class MedCardUpdate(BaseModel):
    patient_name: OptionalNameStr = None

    def map_dict(self) -> dict:
        return self.model_dump(exclude_unset=True)

    def apply_to(self, med_card: MedCardModel) -> None:
        for key, value in self.map_dict().items():
            setattr(med_card, key, value)


class MedCard(MedCardBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)
