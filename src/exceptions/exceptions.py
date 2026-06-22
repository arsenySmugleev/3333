from uuid import UUID


class AppException(Exception):
    status_code = 400
    error_code = "APP_ERROR"

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class DoctorNotFoundException(AppException):
    status_code = 404
    error_code = "DOCTOR_NOT_FOUND"

    def __init__(self, doctor_id: UUID):
        super().__init__(f"Doctor {doctor_id} not found")


class AppointmentNotFoundException(AppException):
    status_code = 404
    error_code = "APPOINTMENT_NOT_FOUND"

    def __init__(self, appointment_id: UUID | None = None):
        if appointment_id is None:
            super().__init__("Appointment not found")
        else:
            super().__init__(f"Appointment {appointment_id} not found")


class PatientNotFoundException(AppException):
    status_code = 404
    error_code = "PATIENT_NOT_FOUND"

    def __init__(self, patient_id: UUID):
        super().__init__(f"Patient {patient_id} not found")


class MedServiceNotFoundException(AppException):
    status_code = 404
    error_code = "MED_SERVICE_NOT_FOUND"

    def __init__(self, med_service_id: UUID | None = None):
        if med_service_id is None:
            super().__init__("MedService not found")
        else:
            super().__init__(f"MedService {med_service_id} not found")


class MedCardNotFoundException(AppException):
    status_code = 404
    error_code = "MED_CARD_NOT_FOUND"

    def __init__(self, med_card_id: UUID):
        super().__init__(f"MedCard {med_card_id} not found")


class InsuranceNotFoundException(AppException):
    status_code = 404
    error_code = "INSURANCE_NOT_FOUND"

    def __init__(self):
        super().__init__("Insurance not found")
