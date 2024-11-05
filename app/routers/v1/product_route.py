from fastapi import APIRouter, Depends, HTTPException, FastAPI, File, UploadFile
from typing import List, Optional
from pydantic import BaseModel, UUID4 
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import PointStruct, VectorParams
from app.utils.logger import log
import uuid
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.databases.psql_db import get_psql_db
from app.databases.qdrant_db import get_qdrant_db, qdrant_client
from app.services import product_service
from app.DTO.product_dto import ProductDTO
import json
import os

    
router = APIRouter(prefix='/api/product')

# create, get, update, delete, product from psql and qdrant.
# curl -X POST http://127.0.0.1:9000/api/product/create_product -H "Content-Type: application/json" -d '{      
#     "name": "black dress for women",
#     "title": "this is a nice dress for women",
#     "description": "description",
#     "price": 123,
#     "rating": 3.3
# }'
@router.post("/create_product")
async def create_product(productDTO: ProductDTO, psql_db_session: AsyncSession = Depends(get_psql_db)):
    log.info(f"Creating product {productDTO.name}")
    product = await product_service.create_product(productDTO, psql_db_session)
    return {"message": "Product created successfully"}

@router.get("/get_product/{product_id}")
async def get_product(product_id: UUID4, psql_db_session: AsyncSession = Depends(get_psql_db)):
    log.info(f"Getting product {product_id}")
    product = await product_service.get_product(product_id, psql_db_session)
    return {"message": "Product retrieved successfully"}

@router.post("/update_product")
async def update_product(product: ProductDTO, psql_db_session: AsyncSession = Depends(get_psql_db)):
    log.info(f"Updating product {product.name}")
    product = await product_service.update_product(product, psql_db_session)
    # TODO: update product in qdrant
    return {"message": "Product updated successfully"}

@router.delete("/delete_product/{product_id}")
async def delete_product(product_id: UUID4, psql_db_session: AsyncSession = Depends(get_psql_db)):
    log.info(f"Deleting product {product_id}")
    await product_service.delete_product(product_id, psql_db_session)
    # TODO: delete product in qdrant
    return {"message": "Product deleted successfully"} 
