from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import api
from app.services.ingestion_service import IngestionService

def get_application():
    app = FastAPI(
        root_path="/ingestion",
        docs_url="/docs",
        openapi_url="/openapi.json"
    )
    app.add_middleware(
        CORSMiddleware,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    app.include_router(api.router)
    return app

app = get_application()