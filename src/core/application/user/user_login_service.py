from dataclasses import dataclass
from datetime import datetime

from core.domain.entities.user import UserName
from core.domain.exceptions import UserDoesNotExistsException
from core.domain.repositories.user_repository import UserRepository


@dataclass
class UserLoginService:
    user_repository: UserRepository

    async def __call__(self, user_name: str, password: str) -> bool:

        user = await self.user_repository.get_by_name(UserName(user_name))
        if not user:
            raise UserDoesNotExistsException(
                f"Non existing user with {user_name} name."
            )

        is_valid = user.name.value == user_name and user.password.value == password

        if is_valid:
            await self.user_repository.update_last_login(
                user_id=user.id,
                last_login=datetime.now(),
            )
        return is_valid
