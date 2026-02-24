import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeMeta, Mapped, declarative_base, mapped_column, relationship


metadata = sa.MetaData()


class BaseServiceModel:

    @classmethod
    def on_conflict_constraint(cls) -> tuple | None:
        return None


Base: DeclarativeMeta = declarative_base(metadata=metadata, cls=BaseServiceModel)


class Doctor(Base):
    __tablename__ = "doctors"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sa.String())

    appointment: Mapped[List["Appointment"]] = relationship(back_populates="doctor", cascade="all, delete-orphan")

class Appointment(Base):
    __tablename__ = "appointments"
    id: Mapped[int] = mapped_column(primary_key=True)
    doc_id: Mapped[int] = mapped_column(ForeignKey("doctors.id"), ondelete="CASCADE")
    time_start: Mapped[datetime.datetime] = mapped_column(sa.DateTime())
    patient_id: Mapped[int] = mapped_column(ForeignKey('patients.id'), ondelete="CASCADE")
    med_service_id: Mapped[int] = mapped_column(ForeignKey('med_services.id'), ondelete="CASACADE")

    doctor: Mapped["Doctor"] = relationship(back_populates="appointment")
    patient: Mapped["Patient"] = relationship(back_populates="appointment")
    med_service: Mapped["MedService"] = relationship(back_populates="appointment")

class Patient(Base):
    __tablename__ = "patients"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sa.String())

    appappointment: Mapped[List["Appointment"]] = relationship(backpopulates="patient", cascade="all, delete-orphan")

class MedService(Base):
    __tablename__ = "med_services"
    id: Mapped[int] = mapped_column(primary_key=True)
    service_name: Mapped[str] = mapped_column(sa.String())

    appappointment: Mapped[List["Appointment"]] = relationship(backpopulates="med_service", cascade="all, delete-orphan")

class MedCard(Base):
    __tablename__ = "med_cards"
    id: Mapped[int] = mapped_column(primary_key=True)
    insurance_id: Mapped[int] = mapped_column(unique=True, nullable=False)

    insurance: Mapped[Optional["Insurance"]] = relationship(back_populates="med_card", uselist=False, cascade="all, delete-orphan")

class Insurance(Base):
    __tablename__ = "insurances"
    id: Mapped[int] = mapped_column(primary_key=True)
    med_card_id: Mapped[int] = mapped_column(ForeignKey('med_cards.id'), ondelete="CASCADE")

    med_card: Mapped["MedCard"] = relationship(back_populates="insurance")
