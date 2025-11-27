from abc import ABC, abstractmethod
from typing import Any, Generic, Optional, TypeVar
from pydantic import BaseModel


T = TypeVar('T')  # Model type
CreateSchema = TypeVar('CreateSchema', bound=BaseModel)  # Input type
UpdateSchema = TypeVar('UpdateSchema', bound=BaseModel)  # Update type


class AbstractCRUD(Generic[T, CreateSchema, UpdateSchema], ABC):
    """Abstract base class for CRUD operations."""

    @classmethod
    async def create_crud(cls)\
            -> 'AbstractCRUD[T, CreateSchema, UpdateSchema]':
        """factory method to create CRUD instance."""
        return cls()  # for simplicity, just return an instance of the class

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
