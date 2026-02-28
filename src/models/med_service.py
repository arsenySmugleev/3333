from typing import List
from src.models.associations import patient_med_service_association

import sqlalchemy as sa
from src.models.patient import Patient
from src.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class MedService(Base):
    __tablename__ = "med_services"
    id: Mapped[int] = mapped_column(primary_key=True)
    service_name: Mapped[str] = mapped_column(sa.String())

    patients: Mapped[List["Patient"]] = relationship(secondary=patient_med_service_association,
                                                     backpopulates="med_service",
                                                     ondelete="all, delete")
