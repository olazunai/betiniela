from dataclasses import dataclass
from typing import Optional

import requests

from src.infrastructure.supabase.exceptions import SupabaseException
from src.core.domain.entities.ranking import Ranking, RankingID, RankingPoints
from src.core.domain.entities.user import UserID
from src.core.domain.repositories.ranking_repository import RankingRepository
from src.core.domain.value_objects.week import Week


@dataclass
class SupabaseRankingRepository(RankingRepository):
    base_url: str
    api_key: str
    table: str = "rankings"

    @property
    def _auth_header(self) -> dict:
        return {
            "apikey": self.api_key,
        }

    @property
    def _url(self) -> str:
        return f"{self.base_url}/{self.table}"

    def add(self, ranking: Ranking) -> None:
        result = requests.post(
            url=self._url, headers=self._auth_header, data=ranking.serialize()
        )

        if result.status_code != 201:
            raise SupabaseException(result.text)

    def add_or_update(self, ranking: Ranking) -> None:
        headers = self._auth_header
        headers["Prefer"] = "resolution=merge-duplicates"

        result = requests.post(url=self._url, headers=headers, data=ranking.serialize())

        if result.status_code != 201:
            raise SupabaseException(result.text)

    def get_by_id(self, ranking_id: RankingID) -> Optional[Ranking]:
        url = f"{self._url}?id=eq.{str(ranking_id.value)}"

        result = requests.get(url=url, headers=self._auth_header)

        if result.status_code != 200:
            raise SupabaseException(result.text)

        if not result.json():
            return None

        return Ranking.deserialize(result.json()[0])

    def get(self, week: Week = None, user_id: UserID = None) -> list[Ranking]:
        params = []

        if week is not None:
            params.append(f"week=eq.{week.serialize()}")

        if user_id is not None:
            params.append(f"user_id=eq.{str(user_id.value)}")

        params.append("order=points.desc")
        query_params = "&".join(params)

        url = f"{self._url}?{query_params}"

        result = requests.get(url=url, headers=self._auth_header)

        if result.status_code != 200:
            raise SupabaseException(result.text)

        return [Ranking.deserialize(data) for data in result.json()]

    def update_points(self, ranking_id: RankingID, points: RankingPoints) -> None:
        url = f"{self._url}?id=eq.{str(ranking_id.value)}"
        result = requests.patch(
            url=url, headers=self._auth_header, data={"points": points.value}
        )

        if result.status_code != 204:
            raise SupabaseException(result.text)
