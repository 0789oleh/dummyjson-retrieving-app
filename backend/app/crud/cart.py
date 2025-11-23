# backend/app/crud/cart.py
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from app.models.cart import Cart, CartItem
from app.schemas.cart import CartCreate, CartUpdate
from typing import List, Optional


async def get_carts(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(Cart)
        .options(joinedload(Cart.items).joinedload(CartItem.product))
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().unique().all()


async def get_cart_by_id(db: AsyncSession, cart_id: int) -> Optional[Cart]:
    result = await db.execute(
        select(Cart)
        .options(joinedload(Cart.items).joinedload(CartItem.product))
        .where(Cart.id == cart_id)
    )
    return result.scalars().unique().first()


async def create_cart(db: AsyncSession, cart_in: CartCreate) -> Cart:
    # Создаём саму корзину
    db_cart = Cart(user_id=cart_in.user_id)
    db.add(db_cart)
    await db.flush()  # чтобы появился cart.id

    # Создаём товары в корзине
    for item in cart_in.items:
        db_item = CartItem(
            cart_id=db_cart.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(db_item)

    await db.flush()
    await db.refresh(db_cart)  # подгружаем связи
    return db_cart


async def get_carts_by_user_id(db: AsyncSession, user_id: int)\
      -> List[Cart]:
    result = await db.execute(
        select(Cart)
        .options(joinedload(Cart.items).joinedload(CartItem.product))
        .where(Cart.user_id == user_id)
        .order_by(Cart.id.desc())
    )
    return result.scalars().unique().all()


async def update_cart(db: AsyncSession, cart_id: int, cart_update: CartUpdate)\
        -> Optional[Cart]:
    db_cart = await get_cart_by_id(db, cart_id)
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


async def delete_cart(db: AsyncSession, cart_id: int) -> bool:
    db_cart = await get_cart_by_id(db, cart_id)
    if not db_cart:
        return False
    await db.delete(db_cart)
    await db.flush()
    return True
