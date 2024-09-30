from fastapi import APIRouter, Depends, HTTPException, FastAPI
from typing import List, Optional
from pydantic import BaseModel, UUID4
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import PointStruct, VectorParams
from app.utils.logger import log
import uuid
from app.config import settings


qd_client = QdrantClient(url=f"{0}:{0}")

class Collection(BaseModel):
    name: str
    size: int
    distance: Optional[models.Distance] = models.Distance.COSINE
    
class Point(BaseModel):
    id: Optional[UUID4] = uuid.uuid4()
    vector: List[float]
    payload: Optional[dict] = {} # we can add prev_chunck_id, next_chunk_id, url, chunk, psql_id
    
class QueryPoint(BaseModel):
    vector: List[float]
    top: Optional[int] = 10
    

def create_collection(collection: Collection):
    log.info(f"Creating collection {collection.name}")
    try:
        collection = qd_client.create_collection(
            collection_name=collection.name,
            vectros_config=models.VectorsParams(
                size=collection.size,
                distance=collection.distance
            )
        )
        return collection
    except Exception as e:
        log.error(f"Error creating collection: {e}")
        raise HTTPException(status_code=400, detail="Error creating collection")
        

def update_collection(collection: Collection):
    log.info(f"Updating collection {collection.name}")
    try:
        collection = qd_client.update_collection(
            collection_name=collection.name,
            vectros_config=models.VectorsParams(
                size=collection.size,
                distance=collection.distance
            )
        )
        return collection
    except Exception as e:
        log.error(f"Error updating collection: {e}")
        raise HTTPException(status_code=400, detail="Error updating collection")

def get_collection(collection_name: str):
    log.info(f"Getting collection {collection_name}")
    try:
        collection = qd_client.get_collection(collection_name=collection_name)
        return collection
    except Exception as e:
        log.error(f"Error getting collection: {e}")
        raise HTTPException(status_code=400, detail="Error getting collection")
    
def get_collections():
    log.info(f"Getting all collections")
    try:
        collections = qd_client.get_collections()
        return collections
    except Exception as e:
        log.error(f"Error getting collections: {e}")
        raise HTTPException(status_code=400, detail="Error getting collections")
    
def delete_collection(collection_name: str):
    log.info(f"Deleting collection {collection_name}")
    try:
        collection = qd_client.delete_collection(collection_name=collection_name)
        return collection
    except Exception as e:
        log.error(f"Error deleting collection: {e}")
        raise HTTPException(status_code=400, detail="Error deleting collection")
    
def add_point(collection_name: str, point: Point):
    log.info(f"Adding point to collection {collection_name}")
    try:
        point = qd_client.upsert(
            collection_name=collection_name,
            points=[models.PointStruct(
                id=str(point.id),
                vector={"text":point.vector},
                payload=point.payload
            )]
        )
        return point
    except Exception as e:
        log.error(f"Error adding point: {e}")
        raise HTTPException(status_code=400, detail="Error adding point")

def update_point(collection_name: str, point: Point):
    pass

def get_point(collection_name: str, id: str):
    try:
        points = qd_client.retrieve(
            collection_name=collection_name,
            ids=[id]
        )
        return points
    except Exception as e:
        log.error(f"Error getting point: {e}")
        raise HTTPException(status_code=400, detail="Error getting point")
    
def get_all_points(collection_name: str):
    try:
        points = qd_client.search(
            collection_name=collection_name,
            query_vector=[0,0,0,0],
            limit=100
        )
        return points
    except Exception as e:
        log.error(f"Error getting all points: {e}")
        raise HTTPException(status_code=400, detail="Error getting all points")
    
def get_point(collection_name: str, query: QueryPoint):
    try:
        points = qd_client.search(
            collection_name=collection_name,
            query_vector=query.vector,
            limit=query.top
        )
        return points
    except Exception as e:
        log.error(f"Error getting points: {e}")
        raise HTTPException(status_code=400, detail="Error getting points")
    
def delete_point(collection_name: str, id: str):
    try:
        points = qd_client.delete(
            collection_name=collection_name,
            points_selector=models.PointIdsList(
                points=[id]
            )
        )
        return points
    except Exception as e:
        log.error(f"Error deleting point: {e}")
        raise HTTPException(status_code=400, detail="Error deleting point")
    
