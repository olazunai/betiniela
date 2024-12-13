from dataclasses import dataclass
from uuid import UUID

from src.core.domain.entities.user import User, UserID
from src.core.domain.exceptions import UserDoesNotExistsException
from src.core.domain.repositories.user_repository import UserRepository


@dataclass
class UserRetrieverService:
    user_repository: UserRepository

    def __call__(self, user_id: UUID) -> User:

        user = self.user_repository.get_by_id(UserID(user_id))
        if not user:
            raise UserDoesNotExistsException(f"Non existing user with {user_id} ID.")

        return user
