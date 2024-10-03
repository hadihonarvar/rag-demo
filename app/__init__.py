from fastapi import FastAPI
from app.routers.v1 import qdrant_collection_route


def create_app() -> FastAPI:
    app = FastAPI()
    # app.include_router(test_route.router, tags=['test'])
    app.include_router(qdrant_collection_route.router, tags=['qdrant'])
    return app
