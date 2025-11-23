# backend/app/services/dummy_loader.py
import httpx
import logging
from sqlalchemy import select

from app.database import async_session
from app.models.user import User
from app.models.product import Product
from app.models.cart import Cart, CartItem

logger = logging.getLogger(__name__)


async def load_initial_data():
    async with async_session() as db:
        # Проверяем, есть ли уже данные
        result = await db.execute(select(User).limit(1))
        if result.scalar_one_or_none():
            logger.info("БД уже содержит данные — пропускаем загрузку")
            return

        logger.info("БД пустая — загружаем данные с dummyjson.com")

        async with httpx.AsyncClient() as client:
            # 1. Сначала пользователи
            resp = await client.get("https://dummyjson.com/users")
            users_data = resp.json()["users"]
            user_id_map = {}  # ← сохраняем mapping dummyjson_id → наш id
            for u in users_data:
                user = User(
                    firstName=u["firstName"],
                    lastName=u["lastName"],
                    email=u["email"],
                )
                db.add(user)
                await db.flush()  # получаем id
                user_id_map[u["id"]] = user.id
            await db.commit()
            logger.info(f"Загружено {len(users_data)} пользователей")

            # 2. Потом продукты
            resp = await client.get("https://dummyjson.com/products")
            products_data = resp.json()["products"]
            product_id_map = {}
            for p in products_data:
                product = Product(
                    title=p["title"],
                    description=p.get("description", ""),
                    price=p["price"],
                )
                db.add(product)
                await db.flush()
                product_id_map[p["id"]] = product.id
            await db.commit()
            logger.info(f"Загружено {len(products_data)} товаров")

            # 3. Наконец корзины — только для существующих пользователей!
            resp = await client.get("https://dummyjson.com/carts")
            carts_data = resp.json()["carts"]
            loaded_carts = 0
            for c in carts_data:
                original_user_id = c["userId"]
                if original_user_id not in user_id_map:
                    logger.warning(f"Пропускаем корзину — userId={original_user_id} не существует")
                    continue

                cart = Cart(user_id=user_id_map[original_user_id])
                db.add(cart)
                await db.flush()

                for item in c["products"]:
                    if item["id"] not in product_id_map:
                        continue  # на случай, если продукта нет
                    db.add(CartItem(
                        cart_id=cart.id,
                        product_id=product_id_map[item["id"]],
                        quantity=item["quantity"],
                    ))
                loaded_carts += 1

            await db.commit()
            logger.info(f"Загружено {loaded_carts} корзин (из {len(carts_data)})")

        logger.info("Данные с dummyjson.com успешно загружены!")
