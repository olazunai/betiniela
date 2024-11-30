from datetime import date, time
import datetime
from typing import Optional
from uuid import UUID
from attr import dataclass


@dataclass
class UserID:
    value: UUID


@dataclass
class UserName:
    value: str


@dataclass
class UserEmail:
    value: str


@dataclass
class UserPassword:
    value: str


@dataclass
class UserHasAnswered:
    value: bool


@dataclass
class User:
    id: UserID
    name: UserName
    email: UserEmail
    password: UserPassword
    last_login: datetime
    has_answered: UserHasAnswered
