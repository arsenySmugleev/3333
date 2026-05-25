from typing import Optional
from pydantic import BaseModel, ConfigDict


class InsuranceBase(BaseModel):
    med_card_id: int
    policy_number: int


class InsuranceCreate(InsuranceBase):
    pass


class InsuranceUpdate(BaseModel):
    policy_number: Optional[int] = None


class Insurance(InsuranceBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
