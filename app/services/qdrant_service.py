from fastapi import APIRouter, Depends, HTTPException, FastAPI
from typing import List, Optional
from pydantic import BaseModel, UUID4
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import PointStruct, VectorParams
from app.utils.logger import log
import uuid
from app.databases.qdrant_db import get_qdrant_db, qdrant_client
# from app.config import settings




class Collection(BaseModel):
    name: str
    size: int
    distance: Optional[models.Distance] = models.Distance.COSINE
    
class Point(BaseModel):
    id: Optional[UUID4] = uuid.uuid4()
    vector: List[float]
    payload: Optional[dict] = {} # customize metadata for filtering if needed.
    
class QueryPoint(BaseModel):
    vector: List[float]
    top: Optional[int] = 10
    

async def create_collection(collection: Collection):
    log.info(f"Creating collection {collection.name}")
    try:
        collection = qdrant_client.create_collection(
            collection_name=collection.name,
            vectors_config=models.VectorParams(
                size=collection.size,
                distance=collection.distance
            )
        )
        return collection
    except Exception as e:
        log.error(f"Error creating collection: {e}")
        raise HTTPException(status_code=400, detail="Error creating collection")
        

async def update_collection(collection: Collection):
    log.info(f"Updating collection {collection.name}")
    try:
        collection = qdrant_client.update_collection(
            collection_name=collection.name,
            vectors_config=models.VectorParams(
                size=collection.size,
                distance=collection.distance
            )
        )
        return collection
    except Exception as e:
        log.error(f"Error updating collection: {e}")
        raise HTTPException(status_code=400, detail="Error updating collection")

async def get_collection(collection_name: str):
    log.info(f"Getting collection {collection_name}")
    try:
        collection = qdrant_client.get_collection(collection_name=collection_name)
        return collection
    except Exception as e:
        log.error(f"Error getting collection: {e}")
        raise HTTPException(status_code=400, detail="Error getting collection")
    
async def collection_exists(collection_name:str):
    log.info(f"Checking if collection exists {collection_name}")
    try:
        collection = qdrant_client.collection_exists(collection_name="{collection_name}")
        return collection
    except Exception as e:
        log.error(f"Error getting collection: {e}")
        raise HTTPException(status_code=400, detail="Error getting collection")

async def get_collections():
    log.info(f"Getting all collections...")
    try:
        collections = qdrant_client.get_collections()
        log.info(f"collections: {collections}")
        return collections
    except Exception as e:
        log.error(f"Error getting collections: {e}")
        raise HTTPException(status_code=400, detail="Error getting collections")
    
async def delete_collection(collection_name: str):
    log.info(f"Deleting collection {collection_name}")
    try:
        collection = qdrant_client.delete_collection(collection_name=collection_name)
        return collection
    except Exception as e:
        log.error(f"Error deleting collection: {e}")
        raise HTTPException(status_code=400, detail="Error deleting collection")
    
async def add_point(collection_name: str, point: Point):
    log.info(f"Adding point to collection {collection_name}")
    try:
        point = qdrant_client.upsert(
            collection_name=collection_name,
            points=[models.PointStruct(
                id=str(point.id),
                vector=point.vector,
                payload=point.payload
            )]
        )
        return point
    except Exception as e:
        log.error(f"Error adding point: {e}")
        raise HTTPException(status_code=400, detail="Error adding point")
    
async def add_points(collection_name: str, points: List[Point]):
    log.info(f"Adding points to collection {collection_name}")
    log.info(f"points: {points}")
    try:
        return qdrant_client.upload_points(
            collection_name=collection_name,
            points=points
        )
    except Exception as e:
        log.error(f"Error adding points: {e}")
        raise HTTPException(status_code=400, detail="Error adding points")

async def update_point(collection_name: str, point: Point):
    pass

async def get_point(collection_name: str, id: str):
    try:
        points = qdrant_client.retrieve(
            collection_name=collection_name,
            ids=[id]
        )
        return points
    except Exception as e:
        log.error(f"Error getting point: {e}")
        raise HTTPException(status_code=400, detail="Error getting point")
    
async def search(collection_name: str, query_vector: List[float], limit: Optional[int] = 10):
    log.info(f"Searching for vetor: {query_vector}")
    try:
        points = qdrant_client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit
        )
        return points
    except Exception as e:
        log.error(f"Error getting points: {e}")
        raise HTTPException(status_code=400, detail="Error getting points")
    
async def get_all_points(collection_name: str):
    try:
        points = qdrant_client.search(
            collection_name=collection_name,
            query_vector=[0] * 1536,
            limit=100
        )
        return points
    except Exception as e:
        log.error(f"Error getting all points: {e}")
        raise HTTPException(status_code=400, detail="Error getting all points")
    
async def delete_point(collection_name: str, id: str):
    try:
        points = qdrant_client.delete(
            collection_name=collection_name,
            points_selector=models.PointIdsList(
                points=[id]
            )
        )
        return points
    except Exception as e:
        log.error(f"Error deleting point: {e}")
        raise HTTPException(status_code=400, detail="Error deleting point")
    
