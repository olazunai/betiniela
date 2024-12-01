from datetime import datetime
from enum import StrEnum
from uuid import UUID
from dataclasses import dataclass


@dataclass
class UserID:
    value: UUID


@dataclass
class UserName:
    value: str


@dataclass
class UserPassword:
    value: str


class UserRole(StrEnum):
    SUPERUSER = "superuser"
    ADMIN = "admin"
    USER = "user"


@dataclass
class UserHasAnswered:
    value: bool


@dataclass
class User:
    id: UserID
    name: UserName
    password: UserPassword
    role: UserRole
    last_login: datetime
    has_answered: UserHasAnswered

    def serialize(self) -> dict:
        return {
            "id": str(self.id.value),
            "name": self.name.value,
            "password": self.password.value,
            "role": self.role.value,
            "last_login": self.last_login.isoformat(),
            "has_answered": self.has_answered.value,
        }

    @classmethod
    def deserialize(cls, obj: dict) -> "User":
        return cls(
            id=UserID(UUID(obj["id"])),
            name=UserName(obj["name"]),
            password=UserPassword(obj["password"]),
            role=UserRole(obj["role"]),
            last_login=datetime.fromisoformat(obj["last_login"]),
            has_answered=UserHasAnswered(obj["has_answered"]),
        )
