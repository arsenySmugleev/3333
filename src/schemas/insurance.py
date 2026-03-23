from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, ConfigDict


class InsuranceBase(BaseModel):
    med_card_id: int


class InsuranceCreate(InsuranceBase):
    pass


class InsuranceUpdate(BaseModel):
    med_card_id: Optional[int] = None


class Insurance(InsuranceBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
