from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import models
from app.database.database import engine
from app.routes import api

def get_application():
    models.Base.metadata.create_all(bind=engine)
    app = FastAPI(
        root_path="/db",
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