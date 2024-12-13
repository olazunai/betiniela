import base64
from dataclasses import dataclass
import json
from random import random
from typing import Optional

from src.core.application.user.user_login_service import UserLoginService
from src.core.domain.entities.user import User
from src.core.domain.exceptions import UserDoesNotExistsException


@dataclass
class AuthService:
    user_login_service: UserLoginService

    def validate_token(self, token: str) -> Optional[User]:
        try:
            user_data = json.loads(base64.b64decode(token))
        except:
            return None

        try:
            user = self.user_login_service(
                user_name=user_data["user"],
                password=user_data["password"],
            )
        except UserDoesNotExistsException:
            return None

        return user

    def generate_token(self, user: User) -> str:
        user_data = {
            "user": user.name.value,
            "password": user.password.value,
            "random": random(),
        }
        return base64.b64encode(json.dumps(user_data).encode("utf-8")).decode("utf-8")
