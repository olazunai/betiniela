from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import requests

from src.infrastructure.supabase.exceptions import SupabaseException
from src.core.domain.entities.user import User, UserHasAnswered, UserID, UserName
from src.core.domain.repositories.user_repository import UserRepository


@dataclass
class SupabaseUserRepository(UserRepository):
    base_url: str
    api_key: str
    table: str = "users"

    @property
    def _auth_header(self) -> dict:
        return {
            "apikey": self.api_key,
            # "Authorization": f"Bearer {self.api_key}"
        }

    @property
    def _url(self) -> str:
        return f"{self.base_url}/{self.table}"

    def add(self, user: User) -> None:
        result = requests.post(
            url=self._url, headers=self._auth_header, data=user.serialize()
        )

        if result.status_code != 201:
            raise SupabaseException(result.text)

    def get_by_id(self, user_id: UserID) -> Optional[User]:
        url = f"{self._url}?id=eq.{str(user_id.value)}"

        result = requests.get(url=url, headers=self._auth_header)

        if result.status_code != 200:
            raise SupabaseException(result.text)

        if not result.json():
            return None

        return User.deserialize(result.json()[0])

    def get_by_name(self, name: UserName) -> Optional[User]:
        url = f"{self._url}?name=eq.{name.value}"

        result = requests.get(url=url, headers=self._auth_header)

        if result.status_code != 200:
            raise SupabaseException(result.text)

        if not result.json():
            return None

        return User.deserialize(result.json()[0])

    def get(self, name: UserName = None) -> list[User]:
        params = []

        if name is not None:
            params.append(f"name=eq.{name.value}")

        params.append("order=name.asc")
        query_params = "&".join(params)

        url = f"{self._url}?{query_params}"

        result = requests.get(url=url, headers=self._auth_header)

        if result.status_code != 200:
            raise SupabaseException(result.text)

        return [User.deserialize(data) for data in result.json()]

    def update_last_login(self, user_id: UserID, last_login: datetime) -> None:
        url = f"{self._url}?id=eq.{str(user_id.value)}"
        result = requests.patch(
            url=url,
            headers=self._auth_header,
            data={"last_login": last_login.isoformat()},
        )

        if result.status_code != 204:
            raise SupabaseException(result.text)

    def update_has_answered(
        self, user_id: UserID, has_answered: UserHasAnswered
    ) -> None:
        url = f"{self._url}?id=eq.{str(user_id.value)}"
        result = requests.patch(
            url=url,
            headers=self._auth_header,
            data={"has_answered": has_answered.value},
        )

        if result.status_code != 204:
            raise SupabaseException(result.text)
