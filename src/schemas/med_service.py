from typing import Optional
from pydantic import BaseModel, ConfigDict


class MedServiceBase(BaseModel):
    service_name: str


class MedServiceCreate(MedServiceBase):
    pass


class MedServiceUpdate(BaseModel):
    service_name: Optional[str] = None


class MedService(MedServiceBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
