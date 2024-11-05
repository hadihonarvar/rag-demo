from pydantic import UUID4
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product_model import Product
from app.DTO.product_dto import ProductDTO
from app.utils.logger import log


class ProductDAO:
    @staticmethod
    async def create_product(product_dto: ProductDTO, db: AsyncSession):
        product = Product(**product_dto.model_dump())
        log.info(f"Product creating in psql")
        await db.commit()
        await db.refresh(product)
        return product

    @staticmethod
    async def get_product(product_id: UUID4, db: AsyncSession):
        return await db.query(Product).filter(Product.id == product_id).first()

    @staticmethod
    async def update_product(product: ProductDTO, db: AsyncSession):
        product = db.query(Product).filter(Product.id == ProductDTO.id).first()
        if product:
            product.name = ProductDTO.name
            product.title = ProductDTO.title
            product.description = ProductDTO.description
            product.price = ProductDTO.price
            product.rating = ProductDTO.rating
            await db.commit()
            return product
    
    @staticmethod
    async def delete_product(product_id: UUID4, db: AsyncSession):
        await db.delete(db.query(Product).filter(Product.id == product_id).first())     
        await db.commit()
        return {"message": "Product deleted successfully"}