from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from backend.config import settings
from backend.routes import routers
from backend.utils import extend_openapi


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(routers)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.APP_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.openapi_schema = extend_openapi(app)
    return app


app = create_app()
