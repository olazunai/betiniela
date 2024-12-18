from dataclasses import dataclass
from uuid import UUID

from src.core.domain.entities.user import UserHasAnswered, UserID
from src.core.domain.repositories.user_repository import UserRepository


@dataclass
class UserHasNasweredUpdaterService:
    user_repository: UserRepository

    def __call__(self, user_id: UUID, has_answered: bool) -> None:
        self.user_repository.update_has_answered(
            user_id=UserID(user_id),
            has_answered=UserHasAnswered(has_answered),
        )
