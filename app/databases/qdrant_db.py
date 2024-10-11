from qdrant_client import QdrantClient
from app.config import settings
from app.utils.logger import log

# Initialize Qdrant Client
# qdrant_client = QdrantClient(
#     host=settings.DB_QDRANT_HOST,
#     port=settings.DB_QDRANT_PORT,
# )
qdrant_client = QdrantClient(
    url=settings.DB_QDRANT_API_URL,
    api_key=settings.DB_QDRANT_API_KEY,
)

async def get_qdrant_db(app):
    @app.on_event("startup")
    async def startup_event():
        log.info("Connecting to Qdrant")

    @app.on_event("shutdown")
    async def shutdown_event():
        log.info("Disconnecting from Qdrant")
