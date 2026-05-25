from typing import List

from src.schemas.patient import Patient
from src.schemas.med_service import MedService


class PatientWithMedServiceResponse(Patient):
    med_service: List[MedService]
