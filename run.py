from app.utils.logger import log
from app.config import settings
log.info(f"Starting server on {settings}")
import uvicorn
from fastapi import FastAPI
from app.routers.v1 import qdrant_route
from app import create_app
from app.utils.logger import log

app = create_app()

if __name__ == "__main__":
    host = settings.FASTAPI_HOST
    port = int(settings.FASTAPI_PORT)
    log.info(f"Starting server on {host}:{port}")
    
    uvicorn.run(
        "run:app",
        # host=host,
        port=port,
        reload=True,
    )