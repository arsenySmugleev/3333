from sqlalchemy.sql.schema import Table, Column, ForeignKey

from src.models.base import Base

patient_med_service_association = Table(
    "patient_med_service",
    Base.metadata,
    Column("patient_id", ForeignKey("patients.id", ondelete="CASCADE"), primary_key=True),
    Column("med_service_id", ForeignKey("med_services.id", ondelete="CASCADE"), primary_key=True)
)
