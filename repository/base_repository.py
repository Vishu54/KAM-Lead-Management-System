from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar

T = TypeVar("T")


class BaseRepository(ABC):
    @abstractmethod
    async def create(self, **kwargs) -> T:
        pass

    @abstractmethod
    async def get_all(self) -> List[T]:
        pass

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[T]:
        pass

    @abstractmethod
    async def update(self, id: str, data: dict) -> Optional[T]:
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        pass
