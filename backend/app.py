from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI

from backend.routes import routers, create_docs_route
from backend.utils import extend_openapi
from backend.config import settings


def create_app() -> FastAPI:
    app = FastAPI(docs_url=None)
    app.mount("/static", StaticFiles(directory="backend/static"), name="static")
    create_docs_route(app)
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
