from typing import Optional
from pydantic import BaseModel, ConfigDict

from src.models.med_card import MedCard


class InsuranceBase(BaseModel):
    med_card_id: int


class InsuranceCreate(InsuranceBase):
    pass


class InsuranceUpdate(BaseModel):
    med_card_id: Optional[int] = None


class Insurance(InsuranceBase):
    id: int
    med_card: Optional["MedCard"] = None
    model_config = ConfigDict(from_attributes=True)
