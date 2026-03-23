from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from starlette.middleware.cors import CORSMiddleware
from src.handlers.doctor import router as doctor
from src.handlers.appointment import router as appointment
from src.handlers.med_card import router as med_card
from src.handlers.insurance import router as insurance
from src.handlers.patient import router as patient
from src.handlers.med_servise import router as med_servise


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
    app.include_router(doctor)
    app.include_router(appointment)
    app.include_router(patient)
    app.include_router(med_servise)
    app.include_router(med_card)
    app.include_router(insurance)

    return app
