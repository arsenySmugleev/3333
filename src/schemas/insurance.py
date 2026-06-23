from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.models.insurance import Insurance as InsuranceModel
from src.schemas.common import OptionalPolicyNumber, PolicyNumber


class InsuranceMapper:
    def map_data(self) -> "InsuranceModel":
        return InsuranceModel(**self.model_dump())


class InsuranceBase(BaseModel):
    policy_number: PolicyNumber


class InsuranceCreate(InsuranceBase, InsuranceMapper):
    pass


class InsuranceUpdate(BaseModel):
    policy_number: OptionalPolicyNumber = None

    def map_update_dict(self) -> dict:
        return self.model_dump(exclude_unset=True)

    def apply_to(self, insurance: InsuranceModel) -> None:
        for key, value in self.map_update_dict().items():
            setattr(insurance, key, value)


class Insurance(InsuranceBase):
    id: UUID
    med_card_id: UUID
    model_config = ConfigDict(from_attributes=True)
