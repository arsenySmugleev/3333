from typing import List
from src.models.association import patient_med_service_association
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID, uuid4
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from src.models.med_service import MedService
from src.models.base import Base


class Patient(Base):
    __tablename__ = "patients"
    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(sa.String())

    med_service: Mapped[List["MedService"]] = relationship("MedService",
                                                           secondary=patient_med_service_association,
                                                           back_populates="patient")
