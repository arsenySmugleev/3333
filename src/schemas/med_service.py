from typing import List
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.models.med_service import MedService as MedServiceModel
from src.schemas.common import NameStr


class MedServiceMapper:
    def map_data(self) -> "MedServiceModel":
        return MedServiceModel(**self.model_dump())

    @classmethod
    def map_list(cls, med_services_data: List["MedServiceMapper"]) -> List["MedServiceModel"]:
        if not med_services_data:
            return []
        return [
            med_service.map_data()
            for med_service in med_services_data
        ]


class MedServiceBase(BaseModel):
    service_name: NameStr


class MedServiceCreate(MedServiceBase, MedServiceMapper):
    pass


class MedService(MedServiceBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)
