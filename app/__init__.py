from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.v1 import qdrant_collection_route, product_route, search_route, test_route
from app.config import settings
from app.database.qdrant_db import init_qdrant_db
from app.database.psql_db import init_psql_db

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
    app.include_router(qdrant_collection_route.router, tags=['qdrant'])
    # app.include_router(product_route.router, tags=['product'])
    app.include_router(search_route.router, tags=['search'])
    # app.include_router(test_route.router, tags=['test'])

    init_qdrant_db(app)
    init_psql_db(app)

    return app
