from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.product import Product, ProductCreate
from app.crud.base import AbstractCRUD


router = APIRouter(prefix="/products", tags=["products"])
product_crud = AbstractCRUD.create_crud()


@router.get("/", response_model=list[Product])
async def read_products(skip: int = 0, limit: int = 100,
                        db: AsyncSession = Depends(get_db)):
    products = await product_crud.get(db, skip=skip, limit=limit)
    return products


@router.post("/", response_model=Product)
async def create(product_in: ProductCreate,
                 db: AsyncSession = Depends(get_db)):
    return await product_crud.create(db, product_in)


@router.patch("/{product_id}", response_model=Product)
async def update_product_endpoint(
    product_id: int,
    updates: dict,
    db: AsyncSession = Depends(get_db)
):
    product = await product_crud.update(db, product_id, updates)
    if not product:
        raise HTTPException(404, "Product not found")
    return product


@router.delete("/{product_id}", response_model=Product)
async def delete(product_id: int, db: AsyncSession = Depends(get_db)):
    db_product = await product_crud.get_by_id(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return await product_crud.delete(db, product_id)
