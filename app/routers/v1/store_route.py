# from fastapi import APIRouter, Depends, HTTPException, FastAPI, File, UploadFile
# from typing import List, Optional
# from pydantic import BaseModel, UUID4 
# from qdrant_client import QdrantClient, models
# from qdrant_client.http.models import PointStruct, VectorParams
# from app.utils.logger import log
# import uuid
# from sqlalchemy.orm import Session
# from app.databases.psql_db import get_psql_db
# from app.databases.qdrant_db import get_qdrant_db


# class StoreDTO(BaseModel):
#     name: str
#     url: str
    
    
# router = APIRouter(prefix='/api/store')

# @router.post("/create_store")
# async def create_store(store: StoreDTO, psql_db_session: Session = Depends(get_psql_db), qdrant_db_session: QdrantClient = Depends(get_qdrant_db)):
#     log.info(f"Creating store {store.name}")
#     store = await create_store(store, psql_db_session, )
#     return {"message": "Store created successfully"}

# @router.get("/get_store/{store_id}")
# async def get_store(store_id: UUID4, psql_db_session: Session = Depends(get_psql_db), qdrant_db_session: QdrantClient = Depends(get_qdrant_db)):
#     log.info(f"Getting store {store_id}")
#     store = await get_store(store_id, psql_db_session)
#     return {"message": "Store retrieved successfully"}

# @router.post("/update_store")
# async def update_store(store: StoreDTO, psql_db_session: Session = Depends(get_psql_db), qdrant_db_session: QdrantClient = Depends(get_qdrant_db)):
#     log.info(f"Updating store {store.name}")
#     store = await update_store(store, psql_db_session)
#     return {"message": "Store updated successfully"}

# @router.delete("/delete_store/{store_id}")
# async def delete_store(store_id: UUID4, psql_db_session: Session = Depends(get_psql_db), qdrant_db_session: QdrantClient = Depends(get_qdrant_db)):
#     log.info(f"Deleting store {store_id}")
#     await delete_store(store_id, psql_db_session)
#     return {"message": "Store deleted successfully"}

