from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from starlette.middleware.cors import CORSMiddleware
from src.api.v1.doctor_appointment import router as doctor_appointment
from src.api.v1.med_card_insurance import router as med_card_insurance
from src.api.v1.patient_med_service import router as patient_med_service
from errors_handlers import register_exception_handlers


def get_app() -> FastAPI:

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
    app.include_router(doctor_appointment, prefix="/api/v1")
    app.include_router(patient_med_service, prefix="/api/v1")
    app.include_router(med_card_insurance, prefix="/api/v1")

    register_exception_handlers(app)
    return app
