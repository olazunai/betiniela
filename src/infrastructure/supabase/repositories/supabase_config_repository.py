from dataclasses import dataclass
from typing import Optional

import requests

from src.infrastructure.supabase.exceptions import SupabaseException
from src.core.domain.entities.config import Config
from src.core.domain.repositories.config_repository import ConfigRepository
from src.core.domain.value_objects.week import Week


@dataclass
class SupabaseConfigRepository(ConfigRepository):
    base_url: str
    api_key: str
    table: str = "configuration"

    @property
    def _auth_header(self) -> dict:
        return {
            "apikey": self.api_key,
        }

    @property
    def _url(self) -> str:
        return f"{self.base_url}/{self.table}"

    def get(self) -> Config:
        result = requests.get(url=self._url, headers=self._auth_header)

        if result.status_code != 200:
            raise SupabaseException(result.text)

        return Config.deserialize(result.json()[0])

    def update(
        self,
        current_week: Optional[Week] = None,
        right_winner_points: Optional[int] = None,
        right_losser_points: Optional[int] = None,
        started_week: Optional[bool] = None,
    ) -> None:
        url = f"{self._url}?select=id"
        result = requests.get(url=url, headers=self._auth_header)

        config_id = result.json()[0]["id"]

        values = {}

        if current_week is not None:
            values["current_week"] = current_week.serialize()

        if right_winner_points is not None:
            values["right_winner_points"] = right_winner_points

        if right_losser_points is not None:
            values["right_losser_points"] = right_losser_points

        if started_week is not None:
            values["started_week"] = started_week

        if values:
            url = f"{self._url}?id=eq.{config_id}"
            result = requests.patch(url=url, headers=self._auth_header, data=values)

            if result.status_code != 204:
                raise SupabaseException(result.text)
