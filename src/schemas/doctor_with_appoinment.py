from typing import List

from src.schemas.appointment import Appointment
from src.schemas.doctor import Doctor


class DoctorWithAppointmentResponse(Doctor):
    appointment: List[Appointment]
