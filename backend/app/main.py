# backend/app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging
from fastapi.middleware.cors import CORSMiddleware
# ЭТО ВСЁ РЕШИТ — импортируем ВСЕ модели ЯВНО и ДО Base!
from app.models.user import User
from app.models.product import Product
from app.models.cart import Cart, CartItem
from app.models.base import Base  # ← теперь Base точно знает про products!

from app.api.v1.router import api_router
from app.database import engine
from app.services.dummy_loader import load_initial_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Запуск приложения...")
    # Создаём таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # Загружаем данные только если БД пустая
    await load_initial_data()
    logger.info("Приложение готово к работе!")
    yield
    await engine.dispose()


app = FastAPI(
    title="SynergyWay Test Task",
    lifespan=lifespan,
)

app.include_router(api_router)

# ДЕБАГ — покажет, какие таблицы видит SQLAlchemy
logger.info(f"Таблицы в Base.metadata: {list(Base.metadata.tables.keys())}")


# ← ДОБАВЬ ЭТО!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # или ["*"] для теста
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)