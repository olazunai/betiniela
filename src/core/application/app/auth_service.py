from dataclasses import dataclass
import json
from random import random
from typing import Optional
from flet.security import encrypt, decrypt

from core.application.user.user_login_service import UserLoginService
from core.domain.entities.user import User
from core.domain.exceptions import UserDoesNotExistsException


@dataclass
class AuthService:
    user_login_service: UserLoginService
    secret_key: str

    def validate_token(self, token: str) -> Optional[User]:
        try:
            user_data = json.loads(decrypt(token, self.secret_key))
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
        return encrypt(json.dumps(user_data), self.secret_key)
