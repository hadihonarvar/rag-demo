from app.utils.logger import log
from app.config import settings
log.info(f"Starting server on {settings}")
import uvicorn
from fastapi import FastAPI
# from app.databases.postgres import db as psql_db
from app.routers.v1 import qdrant_route
from app import create_app
from app.utils.logger import log

app = create_app()

# @app.on_event("startup")
# async def startup_event():
#     await psql_db.connect()
    
# @app.on_event("shutdown")
# async def shutdown_event():
#     await psql_db.disconnect()
    

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