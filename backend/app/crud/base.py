from abc import ABC, abstractmethod
from typing import Any, Optional


class AbstractCRUD(ABC):
    """Abstract base class for CRUD operations."""

    @classmethod
    async def create_crud(cls) -> 'AbstractCRUD':
        """factory method to create CRUD instance."""
        return cls()  # for simplicity, just return an instance of the class

    @abstractmethod
    async def get(self, obj_in: Any) -> Any:
        """Create a new record."""
        pass

    @abstractmethod
    async def create(self, obj_in: Any) -> Any:
        """Create a new record."""
        pass

    @abstractmethod
    async def get_by_id(self, id: Any) -> Optional[Any]:
        """Read a record by ID."""
        pass

    @abstractmethod
    async def update(self, id: Any, obj_in: Any) -> Any:
        """Update a record by ID."""
        pass

    @abstractmethod
    async def delete(self, id: Any) -> None:
        """Delete a record by ID."""
        pass
