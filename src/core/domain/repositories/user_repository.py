from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from core.domain.entities.user import User, UserID, UserName


class UserRepository(ABC):
    @abstractmethod
    async def add(self, user: User) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: UserID) -> Optional[User]:
        pass

    @abstractmethod
    async def get_by_name(self, name: UserName) -> Optional[User]:
        pass

    @abstractmethod
    async def get(self, name: UserName) -> list[User]:
        pass

    @abstractmethod
    async def update_last_login(self, user_id: UserID, last_login: datetime) -> None:
        pass
