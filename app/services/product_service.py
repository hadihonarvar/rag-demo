from fastapi import APIRouter, Depends, HTTPException, FastAPI
from typing import List, Optional
from pydantic import BaseModel, UUID4
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import PointStruct, VectorParams
from app.utils.logger import log
import uuid
from app.databases.qdrant_db import qdrant_client
from app.models.product_model import Product
from app.services import qdrant_service
from app.services.qdrant_service import Point
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
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


async def create_product(product_dto: ProductDTO, psql_db_session: AsyncSession):
    # create product in psql 
    # create product in qdrant using psql id
    log.info(f"Creating product {product_dto}")
    product = await ProductDAO.create_product(product_dto, psql_db_session)
    log.info(f"Product created in psql")
    product_payload = {
        "psql_id": product.id,
        "price": product.price,
        "rating": product.rating,
        # "store": product.storeId
    }
    prompt = f"Product name: {product.name}, Description: {product.description}, Title: {product.title}"
    product_vector = await openAI_service.get_openAI_embedding(prompt)
    log.info(f"Product vector: {product_vector}")
    product_point = Point(
        id = product.id, 
        vector = product_vector,
        payload = product_payload,
    )
    # c = await qdrant_service.collection_exists(collection_name="products")
    collection = qdrant_service.get_collections()
    log.info(f"Collection: {collection}")
    # add point to qdrant
    qdrant_point = qdrant_service.add_point(collection_name="products", point=product_point)
    log.info(f"Product created in qdrant with id: {qdrant_point}")
    return {"message": "Product created successfully", "product": product, "qdrant_point": qdrant_point}

async def get_product(product_id: UUID4, psql_db_session: AsyncSession):
    log.info(f"Getting product {product_id}")
    product = await ProductDAO.get_product(psql_db_session, product_id)
    return {"message": "Product retrieved successfully", "product": product}

async def update_product(product: ProductDTO, psql_db_session: AsyncSession):
    log.info(f"Updating product {product.name}")
    product = await ProductDAO.update_product(psql_db_session, product.id, product.name, product.price)
    return {"message": "Product updated successfully", "product": product}

async def delete_product(product_id: UUID4, psql_db_session: AsyncSession):
    log.info(f"Deleting product {product_id}")
    await ProductDAO.delete_product(psql_db_session, product_id)
    return {"message": "Product deleted successfully"}
