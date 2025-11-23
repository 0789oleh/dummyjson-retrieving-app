from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime, func
from typing import Optional


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[Optional[DateTime]] = \
        mapped_column(DateTime(timezone=True), server_default=func.now())
