from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import Product
from app.schemas.product import ProductCreate
from app.crud.base import AbstractCRUD


class ProductCRUD(AbstractCRUD):
    """CRUD operations for Product model."""

    async def get(self, db: AsyncSession, skip: int = 0, limit: int = 100)\
            -> list[Product]:
        result = await db.execute(select(Product).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, db: AsyncSession, product: ProductCreate)\
            -> Product:
        db_product = Product(**product.model_dump())
        db.add(db_product)
        await db.flush()
        return db_product

    async def get_by_id(self, db: AsyncSession, product_id: int)\
            -> Optional[Product]:
        result = await db.execute(select(Product)
                                  .where(Product.id == product_id))
        return result.scalar_one_or_none()

    async def update(self, db: AsyncSession, product_id: int, updates: dict)\
            -> Optional[Product]:
        product = await self.get_by_id(db, product_id)
        if not product:
            return None

        for key, value in updates.items():
            if hasattr(product, key):
                setattr(product, key, value)
        await db.commit()
        await db.refresh(product)
        return product

    async def delete(self, db: AsyncSession, product_id: int)\
            -> bool:
        db_product = await self.get_by_id(db, product_id)
        if db_product:
            await db.delete(db_product)
            await db.flush()
            return True
        return False
