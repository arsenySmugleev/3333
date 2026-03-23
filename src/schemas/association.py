from pydantic import BaseModel, ConfigDict


class PatientMedServiceAssociation(BaseModel):
    patient_id: int
    med_service_id: int

    model_config = ConfigDict(from_attributes=True)
