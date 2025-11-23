from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.crud import cart as crud_cart
from app.schemas.cart import Cart, CartCreate, CartUpdate
from app.database import get_db

router = APIRouter(prefix="/carts", tags=["carts"])


@router.get("/", response_model=List[Cart])
async def read_carts(skip: int = 0, limit: int = 100,
                     db: AsyncSession = Depends(get_db)):
    carts = await crud_cart.get_carts(db, skip=skip, limit=limit)
    return carts


@router.get("/user/{user_id}", response_model=List[Cart])
async def read_carts_by_user(user_id: int, db: AsyncSession = Depends(get_db)):
    carts = await crud_cart.get_carts_by_user_id(db, user_id)
    return carts


@router.get("/{cart_id}", response_model=Cart)
async def read_cart(cart_id: int, db: AsyncSession = Depends(get_db)):
    db_cart = await crud_cart.get_cart_by_id(db, cart_id)
    if not db_cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return db_cart


@router.post("/", response_model=Cart, status_code=status.HTTP_201_CREATED)
async def create_cart(cart_in: CartCreate, db: AsyncSession = Depends(get_db)):
    return await crud_cart.create_cart(db, cart_in)


@router.patch("/{cart_id}", response_model=Cart)
async def update_cart(cart_id: int, cart_update: CartUpdate,
                      db: AsyncSession = Depends(get_db)):
    db_cart = await crud_cart.update_cart(db, cart_id, cart_update)
    if not db_cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return db_cart


@router.delete("/{cart_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cart(cart_id: int, db: AsyncSession = Depends(get_db)):
    success = await crud_cart.delete_cart(db, cart_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cart not found")
    return None
