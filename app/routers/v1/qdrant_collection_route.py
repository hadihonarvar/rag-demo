from fastapi import APIRouter, Depends, HTTPException, FastAPI
from typing import List, Optional
from pydantic import BaseModel, UUID4 
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import PointStruct, VectorParams
from app.utils.logger import log
import uuid
from app.services import qdrant_service
from transformers import AutoTokenizer, AutoModel
import torch


router = APIRouter('/qdrant/collections')
client = QdrantClient(hrl='http://localhost:6333')

class Collection(BaseModel):
    name: str
    size: int
    distance: Optional[models.Distance] = models.Distance.COSINE
    
class Point(BaseModel):
    id: Optional[UUID4] = uuid.uuid4()
    vector: List[float]
    payload: Optional[dict] = {}
    
class QueryPoint(BaseModel):
    vector: List[float]
    top: Optional[int] = 10
    
@router.get("")
async def qdrant_root():
    model_name = "huggingface/llama-3b"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    
    def get_embedding(text):
        inputs = tokenizer(text, return_tensors="pt")
        outputs = model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).detach().numpy().tolist()

    text_chunk = "sample product info"
    
    return get_embedding(text_chunk)


# collection operations

# curl -X POST "http://localhost:9000/qdrant/collections/create_collection" -H  "Content-Type: application/json" --data-raw '{"name": "products", "size": 10, "distance": "Cosine"}'
@router.post("/create_collection")
async def create_collection(collection: Collection):
    log.info(f"Creating collection {collection.name}")
    collection = await qdrant_service.create_collection(collection)
    return {"status": "success", "collection": collection}


# TODO: adding proper params
@router.post("/update_collection")
async def update_collection(collection: Collection):
    log.info(f"Updating collection {collection.name}")
    collection = await qdrant_service.update_collection(collection)
    return {"status": "success", "collection": collection}

# curl -X GET "http://localhost:9000/qdrant/collections/get_collections"
@router.get("/get_collections")
async def get_collections():
    log.info(f"Getting all collections")
    collections = await qdrant_service.get_collections()
    return {"status": "success", "collections": collections}

# curl -X GET "http://localhost:9000/qdrant/collections/get_collection?name=products"
@router.get("/get_collection")
async def get_collection(name: str):
    log.info(f"Getting collection {name}")
    collection = await qdrant_service.get_collection(name)
    return {"status": "success", "collection": collection}

# curl -X DELETE "http://localhost:9000/qdrant/collections/delete_collection?name=products"
@router.delete("/delete_collection")
async def delete_collection(name: str):
    log.info(f"Deleting collection {name}")
    collection = await qdrant_service.delete_collection(name)
    return {"status": "success", "collection": collection}

# point operations

# curl -X POST "http://localhost:9000/qdrant/collections/add_point" -H  "Content-Type: application/json" --data-raw '{"collection_name": "products", "point": {"vector": [1, 2, 3], "payload": {"name": "product1"}}}'
@router.post("/add_point")
async def add_point(collection_name: str, point: Point):
    log.info(f"Adding point to collection {collection_name}")
    point = await qdrant_service.add_point(collection_name, point)
    return {"status": "success", "point": point}

# curl -X POST "http://localhost:9000/qdrant/collections/get_point" -H  "Content-Type: application/json" --data-raw '{"collection_name": "products", "id": "1b9d6bcd-bbfd-4b2d-9b5d-ab8dfbbd4bed"}'
@router.post("/get_point")
async def get_point(collection_name: str, id: UUID4):
    log.info(f"Getting point from collection {collection_name}")
    point = await qdrant_service.get_point(collection_name, id)
    return {"status": "success", "point": point}

# curl -X POST "http://localhost:9000/qdrant/collections/get_points" -H  "Content-Type: application/json" --data-raw '{"collection_name": "products", "ids": ["1b9d6bcd-bbfd-4b2d-9b5d-ab8dfbbd4bed"]}'
@router.post("/get_points")
async def get_points(collection_name: str, ids: List[UUID4]):
    log.info(f"Getting points from collection {collection_name}")
    points = await qdrant_service.get_points(collection_name, ids)
    return {"status": "success", "points": points}

# curl -X POST "http://localhost:9000/qdrant/collections/get_all_points" -H  "Content-Type: application/json" --data-raw '{"collection_name": "products"}'
@router.post("/get_all_points")
async def get_all_points(collection_name: str):
    log.info(f"Getting all points from collection {collection_name}")
    points = await qdrant_service.get_all_points(collection_name)
    return {"status": "success", "points": points}

# curl -X POST "http://localhost:9000/qdrant/collections/delete_point" -H  "Content-Type: application/json" --data-raw '{"collection_name": "products", "id": "1b9d6bcd-bbfd-4b2d-9b5d-ab8dfbbd4bed"}'
@router.post("/delete_point")
async def delete_point(collection_name: str, id: UUID4):
    log.info(f"Deleting point from collection {collection_name}")
    point = await qdrant_service.delete_point(collection_name, id)
    return {"status": "success", "point": point}

# curl -X POST "http://localhost:9000/qdrant/collections/query_point" -H  "Content-Type: application/json" --data-raw '{"collection_name": "products", "point": {"vector": [1, 2, 3], "top": 10}}'
@router.post("/query_point")
async def query_point(collection_name: str, point: QueryPoint):
    log.info(f"Querying point from collection {collection_name}")
    points = await qdrant_service.query_point(collection_name, point)
    return {"status": "success", "points": points}