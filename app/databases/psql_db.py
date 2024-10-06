from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.utils.logger import log

DATABASE_URL = f'postgresql+asyncpg://{settings.DB_PSQL_USER}:{settings.DB_PSQL_PASSWORD}@{settings.DB_PSQL_HOST}:{settings.DB_PSQL_PORT}/{settings.DB_PSQL_NAME}'

# Create async engine and session
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

async def get_psql_db():
    async with SessionLocal() as session:
        yield session

async def init_psql_db(app):
    @app.on_event("startup")
    async def startup_event():
        log.info("Connecting to PostgreSQL")

    @app.on_event("shutdown")
    async def shutdown_event():
        # Any shutdown logic for PostgreSQL
        log.info("Disconnecting from PostgreSQL")

