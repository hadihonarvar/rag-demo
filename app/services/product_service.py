from fastapi import APIRouter, Depends, HTTPException, FastAPI
from typing import List, Optional
from pydantic import BaseModel, UUID4
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import PointStruct, VectorParams
from app.utils.logger import log
import uuid
from app.databases.qdrant_db import qdrant_client
from app.models.product_model import Product
from app.services.qdrant_service import Point
from sqlalchemy.orm import Session
from app.services import openAI_service
from app.DTO.product_dto import ProductDTO
from app.DAO.product_dao import ProductDAO


# def create_product_psql(product: Product):
#     log.info(f"Creating product {product.name}")
#     try:
#         product = Product.create(
#             name=product.name,
#             description=product.description,
#             price=product.price,
#             # assets=product.assets,
#             # reviews=product.reviews,
#             # rating=product.rating,
#             # store=product.store
#         )
#         return product
#     except Exception as e:
#         log.error(f"Error creating product: {e}")
#         raise HTTPException(status_code=400, detail="Error creating product")
    
# def create_product_qdrant(product: Product):
#     log.info(f"Creating product {product.name}")
#     try:
#         product_point = PointStruct(
#         )
#         return product_point
#     except Exception as e:
#         log.error(f"Error creating product: {e}")
#         raise HTTPException(status_code=400, detail="Error creating product")


async def create_product(product_dto: ProductDTO, psql_db_session: Session, qdrant_client: QdrantClient):
    # create product in psql
    # create product in qdrant using psql id
    product = await ProductDAO.create_product(product_dto, psql_db_session)
    product_payload = {
        "name": product.name,
        "description": product.description,
        "price": product.price,
        # "assets": product.assets,
        # "reviews": product.reviews,
        # "rating": product.rating,
        # "store": product.store
    }
    prompt = f"Product name: {product.name}, Description: {product.description}"
    product_vector = await openAI_service.get_openAI_embedding(prompt)
    product_point = Point(
        id = product.id, 
        vector = product_vector,
        payload = product_payload
    )
    return {"message": "Product created successfully"}


    
# async def add_point(collection_name: str, point: Point):
#     log.info(f"Adding point to collection {collection_name}")
#     try:
#         point = qdrant_client.upsert(
#             collection_name=collection_name,
#             points=[models.PointStruct(
#                 id=str(point.id),
#                 vector={"text":point.vector},
#                 payload=point.payload
#             )]
#         )
#         return point
#     except Exception as e:
#         log.error(f"Error adding point: {e}")
#         raise HTTPException(status_code=400, detail="Error adding point")

        