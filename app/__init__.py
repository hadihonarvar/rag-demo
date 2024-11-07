from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.v1 import qdrant_route, prompt_route, index_route
from app.config import settings
from app.databases.qdrant_db import get_qdrant_db
from app.utils.logger import log


limiter = None

def create_app() -> FastAPI:
    app = FastAPI()
    # set cors:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=settings.cors_methods,
        allow_headers=settings.cors_headers,
    )

    # include routers
    app.include_router(qdrant_route.router, tags=['qdrant'])
    app.include_router(prompt_route.router, tags=['prompt'])
    app.include_router(index_route.router, tags=['index'])

    return app
