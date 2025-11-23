from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import Product
from app.schemas.product import ProductCreate


async def get_products(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Product).offset(skip).limit(limit))
    return result.scalars().all()


async def create_product(db: AsyncSession, product: ProductCreate):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    await db.flush()
    return db_product
# Добавь get_by_id, update, delete аналогично


async def get_product_by_id(db: AsyncSession, product_id: int):
    result = await db.execute(select(Product).where(Product.id == product_id))
    return result.scalar_one_or_none()


async def update_product(db: AsyncSession, product_id: int, updates: dict)\
      -> Product:
    product = await get_product_by_id(db, product_id)
    if not product:
        return None
    
    for key, value in updates.items():
        if hasattr(product, key):
            setattr(product, key, value)
    
    await db.commit()
    await db.refresh(product)
    return product


async def delete_product(db: AsyncSession, product_id: int):
    db_product = await get_product_by_id(db, product_id)
    if db_product:
        await db.delete(db_product)
        await db.flush()
    return db_product
