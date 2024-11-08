from fastapi import APIRouter, Depends, HTTPException, FastAPI, File, UploadFile
from typing import List, Optional
from pydantic import BaseModel, UUID4 
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import PointStruct, VectorParams
from app.utils.logger import log
import uuid
# from app.services.openAI_service import get_openAI_embedding, get_openAI_image_description
from app.services import qdrant_service, openAI_service
from app.services.openAI_service import get_openAI_embedding


router = APIRouter(prefix='/api/prompt')

class PromptRequest(BaseModel):
    prompt: str
    collection_name: str

# curl -X POST "http://localhost:9000/api/prompt" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"prompt\": \"tell me about company and its mission\", \"collection_name\": \"docs\"}"
@router.post("")
async def prompt_query(request: PromptRequest):
    prompt = request.prompt
    collection_name = request.collection_name
    log.info(f"Getting embedding for prompt: {prompt}")
    prompt_embedding_vector = await openAI_service.get_openAI_embedding(prompt)
    log.info(f"prompt_embedding_vector: {prompt_embedding_vector}")
    nearest_points = await qdrant_service.search(collection_name=collection_name, query_vector=prompt_embedding_vector)
    limit = 2
    log.info(f"nearest_points: {nearest_points}")   
    chunks = [nearest_points[x:x+limit] for x in range(0, len(nearest_points), limit)]
    log.info(f"chunks: {chunks}")
    log.info(f"prompt: {prompt}")

    context_from_chunks = ' '.join(point.payload['chunk'] for sublist in chunks for point in sublist)

    conversation = [
        {"role": "system", "content": "You are a helpful assistant who provides detailed information based on the user's context."},
        {"role": "user", "content": context_from_chunks},
        {"role": "user", "content": prompt}
    ]

    llm_answer = await openAI_service.get_openAI_response(conversation)

    return {
        "retrived_info": context_from_chunks,
        "answer": llm_answer
    }
