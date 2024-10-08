from pydantic import UUID4
from sqlalchemy.orm import Session
from app.models.product_model import Product
from app.DTO.product_dto import ProductDTO


class ProductDAO:
    @staticmethod
    async def create_product(db: Session, product_dto: ProductDTO):
        product_dto.id = UUID4()
        product = Product(**product_dto.dict())
        db.add(product)
        await db.commit()
        await db.refresh(product)
        return product

    @staticmethod
    async def get_product(db: Session, product_id: UUID4):
        return await db.query(Product).filter(Product.id == product_id).first()

    @staticmethod
    async def update_product(db: Session, product_id: UUID4, name: str, price: int):
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            product.name = name
            product.price = price
            await db.commit()
            await db.refresh(product)
        return product
    
    @staticmethod
    async def delete_product(db: Session, product_id: UUID4):
        await db.delete(db.query(Product).filter(Product.id == product_id).first())     
        await db.commit()
        return {"message": "Product deleted successfully"}