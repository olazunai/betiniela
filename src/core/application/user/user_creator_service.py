from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from src.core.domain.entities.user import (
    User,
    UserHasAnswered,
    UserID,
    UserName,
    UserPassword,
    UserRole,
)
from src.core.domain.exceptions import UserAlreadyExistsException
from src.core.domain.repositories.user_repository import UserRepository


@dataclass
class UserCreatorService:
    user_repository: UserRepository

    def __call__(self, user_name: str, password: str) -> User:

        existing_user = self.user_repository.get_by_name(UserName(user_name))
        if existing_user:
            raise UserAlreadyExistsException(
                "Trying to create user with already existing user name."
            )

        user = User(
            id=UserID(uuid4()),
            name=UserName(user_name),
            password=UserPassword(password),
            role=UserRole.USER,
            last_login=datetime.now(),
            has_answered=UserHasAnswered(False),
        )

        self.user_repository.add(user)

        return user
