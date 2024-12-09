from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.core.domain.entities.user import User, UserName
from src.core.domain.exceptions import UserDoesNotExistsException
from src.core.domain.repositories.user_repository import UserRepository


@dataclass
class UserLoginService:
    user_repository: UserRepository

    def __call__(self, user_name: str, password: str) -> Optional[User]:

        user = self.user_repository.get_by_name(UserName(user_name))
        if not user:
            raise UserDoesNotExistsException(
                f"Non existing user with {user_name} name."
            )

        is_valid = user.name.value == user_name and user.password.value == password

        if is_valid:
            self.user_repository.update_last_login(
                user_id=user.id,
                last_login=datetime.now(),
            )
            return user
