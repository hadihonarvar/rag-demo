from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.v1 import qdrant_collection_route, product_route, search_route, test_route
from app.config import settings
from app.databases.qdrant_db import get_qdrant_db
from app.databases.psql_db import get_psql_db
import boto3

config = None
# psql_db = SQLAlchemy()


# migrate = Migrate()
s3 = boto3.client('s3')
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
    app.include_router(qdrant_collection_route.router, tags=['qdrant'])
    app.include_router(product_route.router, tags=['product'])
    app.include_router(search_route.router, tags=['search'])
    # app.include_router(test_route.router, tags=['test'])

    return app
