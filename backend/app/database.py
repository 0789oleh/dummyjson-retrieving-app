from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession,
                                 expire_on_commit=False)

# ← ЭТО САМОЕ ГЛАВНОЕ — ДОБАВЬ ЭТУ СТРОКУ!
async_session = sessionmaker(engine, class_=AsyncSession,
                             expire_on_commit=False)


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
