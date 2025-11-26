from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from app.models.cart import Cart, CartItem
from app.schemas.cart import CartCreate, CartUpdate
from typing import List, Optional

from app.crud.base import AbstractCRUD


class CartCRUD(AbstractCRUD):
    """CRUD operations for Cart and CartItem models."""

    async def get(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        result = await db.execute(
            select(Cart)
            .options(joinedload(Cart.items).joinedload(CartItem.product))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().unique().all()

    async def get_by_id(self, db: AsyncSession, cart_id: int)\
            -> Optional[Cart]:
        result = await db.execute(
            select(Cart)
            .options(joinedload(Cart.items).joinedload(CartItem.product))
            .where(Cart.id == cart_id)
        )
        return result.scalars().unique().first()

    async def create(self, db: AsyncSession, cart_in: CartCreate) -> Cart:
        # Create the cart itself
        db_cart = Cart(user_id=cart_in.user_id)
        db.add(db_cart)
        await db.flush()  # to get cart.id

        # Create items in the cart
        for item in cart_in.items:
            db_item = CartItem(
                cart_id=db_cart.id,
                product_id=item.product_id,
                quantity=item.quantity
            )
            db.add(db_item)

        await db.flush()
        await db.refresh(db_cart)  # load relationships
        return db_cart

    async def get_carts_by_user_id(self, db: AsyncSession, user_id: int)\
            -> List[Cart]:
        result = await db.execute(
            select(Cart)
            .options(joinedload(Cart.items).joinedload(CartItem.product))
            .where(Cart.user_id == user_id)
            .order_by(Cart.id.desc())
        )
        return result.scalars().unique().all()

    async def update(self, db: AsyncSession, cart_id: int,
                     cart_update: CartUpdate) -> Optional[Cart]:
        db_cart = await self.get_by_id(db, cart_id)
        if not db_cart:
            return None

        # Обновляем user_id (если нужно)
        db_cart.user_id = cart_update.user_id

        # Удаляем старые товары
        await db.execute(delete(CartItem).where(CartItem.cart_id == cart_id))

        # Добавляем новые
        for item in cart_update.items:
            db_item = CartItem(
                cart_id=cart_id,
                product_id=item.product_id,
                quantity=item.quantity
            )
            db.add(db_item)
        await db.flush()
        await db.refresh(db_cart)
        return db_cart

    async def delete(self, db: AsyncSession, cart_id: int) -> bool:
        db_cart = await self.get_by_id(db, cart_id)
        if not db_cart:
            return False
        await db.delete(db_cart)
        await db.flush()
        return True
