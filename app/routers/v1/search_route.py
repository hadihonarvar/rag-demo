from fastapi import APIRouter, Depends, HTTPException, FastAPI, File, UploadFile
from typing import List, Optional
from pydantic import BaseModel, UUID4 
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import PointStruct, VectorParams
from app.utils.logger import log
import uuid
# from app.services.openAI_service import get_openAI_embedding, get_openAI_image_description
from app.services import qdrant_service, openAI_service


router = APIRouter(prefix='/api/search')

# curl -X 'GET' 'http://localhost:9000/api/search/search_query?query=blue%20shrit%20form%20men' -H 'accept: application/json'
@router.get("/search_query")
async def search_query(query: str):
    log.info("Getting embedding")
    search_query_embedding_vector = await openAI_service.get_openAI_embedding(query)
    log.info("search_query_embedding_vector: ", search_query_embedding_vector)
    nearest_points = await qdrant_service.search(collection_name="products", query_vector=search_query_embedding_vector)
    return {"nearest points": nearest_points}


@router.post("/search_image")
async def search_image(image: UploadFile = File(...)):
    log.info("Getting embedding1")
    # store file in s3
    image_url = await aws_service.store_image_to_s3(image)
    description = await get_openAI_image_description(image_url)
    nearest_points = await qdrant_service.search_collection(description)
    product_info = await get_product_info_from_points(nearest_points)
    return {"message": "Welcome to Qdrant", "embedding": emb}

@router.post("/search_voice")
async def search_voice(audio: UploadFile = File(...)):
    log.info("Getting embedding1")
    # store file in s3
    voice_url = await aws_service.store_voice_to_s3(audio)
    description = await get_openAI_voice_description(voice_url)
    nearest_points = await qdrant_service.search_collection(description)
    product_info = await get_product_info_from_points(nearest_points)
    return {"message": "Welcome to Qdrant", "embedding": emb}