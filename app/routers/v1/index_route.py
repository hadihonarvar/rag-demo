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
from app.utils.text_processor import text_sanitizer, chunk_doc
from app.services.qdrant_service import Point


router = APIRouter(prefix='/api/index')
'''
curl -X 'POST' 'http://localhost:9000/api/index/add_doc' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{
    "doc": "your long document text here...",    
    "collection_name": "docs"
}'
'''

class DocumentRequest(BaseModel):
    doc: str # can extend to accept file uploads
    collection_name: str

@router.post("/add_doc")
async def add_doc(request: DocumentRequest):
    log.info(f"Adding document to collection: {request.collection_name}")
    doc = request.doc
    collection_name = request.collection_name
    # first needs sanitization - ignored for now.
    sanitized_doc = text_sanitizer(doc)
    chunks = chunk_doc(sanitized_doc)

    # getting embeddings for each chunk
    embeddings = []
    for chunk in chunks:
        log.info(f"Getting embedding for chunk: {chunk}")
        chunk_embedding_vector = await openAI_service.get_openAI_embedding(chunk)
        log.info(f"chunk_embedding_vector: {len(chunk_embedding_vector) }")
        # point = Point(
        #     vector=chunk_embedding_vector,
        #     payload={"chunk": chunk}
        # )
        embeddings.append(chunk_embedding_vector)

    # insert points into qdrant
    points = [models.PointStruct(
                id=str(uuid.uuid4()),
                vector=point[0],
                payload={"chunk":point[1]}
            ) for point in zip(embeddings, chunks)]
    await qdrant_service.add_points(collection_name=collection_name, points=points)

    return {"status": "success", "points": points}