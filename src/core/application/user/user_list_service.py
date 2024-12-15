from dataclasses import dataclass

from src.core.domain.entities.user import User
from src.core.domain.repositories.user_repository import UserRepository


@dataclass
class UserListService:
    user_repository: UserRepository

    def __call__(self) -> list[User]:
        return self.user_repository.get()
