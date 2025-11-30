from abc import ABC, abstractmethod
from typing import Any, Generic, Optional, TypeVar
from pydantic import BaseModel


T = TypeVar('T')  # Model type
CreateSchema = TypeVar('CreateSchema', bound=BaseModel)  # Input type
UpdateSchema = TypeVar('UpdateSchema', bound=BaseModel)  # Update type


class AbstractCRUD(Generic[T, CreateSchema, UpdateSchema], ABC):
    """Abstract base class for CRUD operations."""

    @staticmethod
    def create_crud(crud_cls: type['AbstractCRUD']) -> 'AbstractCRUD':
        return crud_cls()

    @abstractmethod
    async def get(self, obj_in: Any) -> list[T]:
        """Create a new record."""
        pass

    @abstractmethod
    async def create(self, obj_in: Any) -> T:
        """Create a new record."""
        pass

    @abstractmethod
    async def get_by_id(self, id: Any) -> Optional[T]:
        """Read a record by ID."""
        pass

    @abstractmethod
    async def update(self, id: Any, obj_in: Any) -> Optional[T]:
        """Update a record by ID."""
        pass

    @abstractmethod
    async def delete(self, id: Any) -> bool:
        """Delete a record by ID."""
        pass
