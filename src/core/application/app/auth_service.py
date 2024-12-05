from dataclasses import dataclass
import json
from random import random
from typing import Optional
from cryptography.fernet import Fernet, InvalidToken

from core.application.user.user_login_service import UserLoginService
from core.domain.entities.user import User


@dataclass
class AuthService:
    user_login_service: UserLoginService
    secret_key: str

    def validate_token(self, token: str) -> Optional[User]:
        encrypter = Fernet(self.secret_key)
        try:
            user_data = json.loads(encrypter.decrypt(token).decode())
        except InvalidToken:
            return None

        user = self.user_login_service(
            user_name=user_data["user"],
            password=user_data["password"],
        )
        return user

    def generate_token(self, user: User) -> str:
        encrypter = Fernet(self.secret_key)
        user_data = {
            "user": user.name.value,
            "password": user.password.value,
            "random": random(),
        }
        return encrypter.encrypt(json.dumps(user_data).encode()).decode()
