from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from core.domain.entities.user import (
    User,
    UserHasAnswered,
    UserID,
    UserName,
    UserPassword,
    UserRole,
)
from core.domain.exceptions import UserAlreadyExistsException
from core.domain.repositories.user_repository import UserRepository


@dataclass
class UserCreatorService:
    user_repository: UserRepository

    async def __call__(self, user_name: str, password: str) -> None:

        existing_user = await self.user_repository.get_by_name(UserName(user_name))
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

        await self.user_repository.add(user)
