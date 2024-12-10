from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import requests

from src.core.domain.repositories.response_repository import ResponseRepository
from src.infrastructure.supabase.exceptions import SupabaseException
from src.core.domain.entities.match import MatchID
from src.core.domain.entities.response import Response, ResponseID, ResponseLosserPoints
from src.core.domain.entities.user import UserID
from src.core.domain.value_objects.team import Team
from src.core.domain.value_objects.week import Week


@dataclass
class SupabaseResponseRepository(ResponseRepository):
    base_url: str
    api_key: str
    table: str = "responses"

    @property
    def _auth_header(self) -> dict:
        return {
            "apikey": self.api_key,
        }

    @property
    def _url(self) -> str:
        return f"{self.base_url}/{self.table}"

    def add(self, response: Response) -> None:
        result = requests.post(
            url=self._url, headers=self._auth_header, data=response.serialize()
        )

        if result.status_code != 201:
            raise SupabaseException(result.text)

    def get_by_id(self, response_id: ResponseID) -> Optional[Response]:
        url = f"{self._url}?id=eq.{str(response_id.value)}"

        result = requests.get(url=url, headers=self._auth_header)

        if result.status_code != 200:
            raise SupabaseException(result.text)

        if not result.json():
            return None

        return Response.deserialize(result.json()[0])

    def get(
        self, week: Week = None, match_id: MatchID = None, user_id: UserID = None
    ) -> list[Response]:
        params = []

        if week is not None:
            params.append(f"week=eq.{week.serialize()}")

        if match_id is not None:
            params.append(f"match_id=eq.{str(match_id.value)}")

        if user_id is not None:
            params.append(f"user_id=eq.{str(user_id.value)}")

        params.append("order=match_id.desc")
        query_params = '&'.join(params)

        url = f"{self._url}?{query_params}"

        result = requests.get(url=url, headers=self._auth_header)

        if result.status_code != 200:
            raise SupabaseException(result.text)

        return [Response.deserialize(data) for data in result.json()]

    def update_data(
        self, response_id: ResponseID, winner: Team, losser_points: ResponseLosserPoints
    ) -> None:
        values = {
            "losser_points": losser_points.value,
            "winner": winner.value,
            "updated_time": datetime.now().isoformat(),
        }

        url = f"{self._url}?id=eq.{str(response_id.value)}"
        result = requests.patch(url=url, headers=self._auth_header, data=values)

        if result.status_code != 204:
            raise SupabaseException(result.text)
