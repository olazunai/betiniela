from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from core.domain.entities.user import User, UserHasAnswered, UserID, UserName


class UserRepository(ABC):
    @abstractmethod
    def add(self, user: User) -> None:
        pass

    @abstractmethod
    def get_by_id(self, user_id: UserID) -> Optional[User]:
        pass

    @abstractmethod
    def get_by_name(self, name: UserName) -> Optional[User]:
        pass

    @abstractmethod
    def get(self, name: UserName) -> list[User]:
        pass

    @abstractmethod
    def update_last_login(self, user_id: UserID, last_login: datetime) -> None:
        pass

    @abstractmethod
    def update_has_answered(
        self, user_id: UserID, has_answered: UserHasAnswered
    ) -> None:
        pass
