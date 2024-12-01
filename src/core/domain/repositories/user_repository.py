from abc import ABC, abstractmethod
from typing import Optional

from core.domain.entities.user import User, UserID


class UserRepository(ABC):
    @abstractmethod
    async def add(self, user: User) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: UserID) -> Optional[User]:
        pass

    @abstractmethod
    async def get(self) -> list[User]:
        pass
