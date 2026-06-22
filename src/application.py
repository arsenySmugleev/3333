from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from starlette.middleware.cors import CORSMiddleware
from src.controllers.v1.doctors import router as doctor_appointment
from src.controllers.v1.medical_cards import router as med_card_insurance
from src.controllers.v1.patients import router as patient_med_service
from src.exceptions.exception_handler import register_exception_handlers
from logging_config import configure_logging
from request_id_middleware import RequestIdMiddleware


def get_app() -> FastAPI:
    configure_logging()

    app = FastAPI(
        docs_url='/docs',
        openapi_url='/openapi.json',
        default_response_class=UJSONResponse,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    app.add_middleware(RequestIdMiddleware)
    app.include_router(doctor_appointment, prefix="/api/v1")
    app.include_router(patient_med_service, prefix="/api/v1")
    app.include_router(med_card_insurance, prefix="/api/v1")

    register_exception_handlers(app)
    return app
