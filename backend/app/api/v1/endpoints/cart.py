from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.cart import Cart, CartCreate, CartUpdate
from app.database import get_db
from app.crud.base import AbstractCRUD
from app.crud.cart import CartCRUD


class CartController:
    """Controller for Cart endpoints."""

    __router = APIRouter(prefix="/carts", tags=["carts"])
    __cartCRUD: CartCRUD = AbstractCRUD.create_crud()

    @__router.get("/", response_model=List[Cart])
    async def get(self, skip: int = 0, limit: int = 100,
                  db: AsyncSession = Depends(get_db)):
        carts = await self.__cartCRUD.get(db, skip=skip, limit=limit)
        return carts

    @__router.get("/user/{user_id}", response_model=List[Cart])
    async def read_carts_by_user(self, user_id: int,
                                 db: AsyncSession = Depends(get_db)):
        carts = await self.__cartCRUD.get_carts_by_user_id(db, user_id)
        return carts

    @__router.get("/{cart_id}", response_model=Cart)
    async def get_by_id(self, cart_id: int,
                        db: AsyncSession = Depends(get_db)):
        db_cart = await self.__cartCRUD.get_by_id(db, cart_id)
        if not db_cart:
            raise HTTPException(status_code=404, detail="Cart not found")
        return db_cart

    @__router.post("/", response_model=Cart,
                   status_code=status.HTTP_201_CREATED)
    async def create_cart(self, cart_in: CartCreate,
                          db: AsyncSession = Depends(get_db)):
        return await self.__cartCRUD.create(db, cart_in)

    @__router.patch("/{cart_id}", response_model=Cart)
    async def update_cart(self, cart_id: int, cart_update: CartUpdate,
                          db: AsyncSession = Depends(get_db)):
        db_cart = await self.__cartCRUD.update(db, cart_id, cart_update)
        if not db_cart:
            raise HTTPException(status_code=404, detail="Cart not found")
        return db_cart

    @__router.delete("/{cart_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_cart(self, cart_id: int,
                          db: AsyncSession = Depends(get_db)):
        success = await self.__cartCRUD.delete(db, cart_id)
        if not success:
            raise HTTPException(status_code=404, detail="Cart not found")
        return None

    def get_router(self):
        return self.__router
