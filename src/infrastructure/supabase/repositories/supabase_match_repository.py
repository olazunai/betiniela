from dataclasses import dataclass
from datetime import time
from typing import Optional

import requests

from src.infrastructure.supabase.exceptions import SupabaseException
from src.core.domain.entities.match import Match, MatchID, MatchResult
from src.core.domain.repositories.match_repository import MatchRepository
from src.core.domain.value_objects.team import Team
from src.core.domain.value_objects.week import Week


@dataclass
class SupabaseMatchRepository(MatchRepository):
    base_url: str
    api_key: str
    table: str = "matches"

    @property
    def _auth_header(self) -> dict:
        return {
            "apikey": self.api_key,
        }

    @property
    def _url(self) -> str:
        return f"{self.base_url}/{self.table}"

    def add(self, match: Match) -> None:
        result = requests.post(
            url=self._url, headers=self._auth_header, data=match.serialize()
        )

        if result.status_code != 201:
            raise SupabaseException(result.text)

    def get_by_id(self, match_id: MatchID) -> Optional[Match]:
        url = f"{self._url}?id=eq.{str(match_id.value)}"

        result = requests.get(url=url, headers=self._auth_header)

        if result.status_code != 200:
            raise SupabaseException(result.text)

        if not result.json():
            return None

        return Match.deserialize(result.json()[0])

    def delete(self, match_id: MatchID) -> None:
        url = f"{self._url}?id=eq.{str(match_id.value)}"

        result = requests.delete(url=url, headers=self._auth_header)

        if result.status_code != 200:
            raise SupabaseException(result.text)

    def get(self, week: Week = None) -> list[Match]:
        params = []
        if week is not None:
            params.append(f"week=eq.{week.serialize()}")

        params.append("order=match_day.asc,match_time.asc")
        query_params = "&".join(params)

        url = f"{self._url}?{query_params}"
        result = requests.get(url=url, headers=self._auth_header)

        if result.status_code != 200:
            raise SupabaseException(result.text)

        return [Match.deserialize(data) for data in result.json()]

    def update(
        self,
        match_id: MatchID,
        match_time: Optional[time] = None,
        local_team: Optional[Team] = None,
        visitor_team: Optional[Team] = None,
        result: Optional[MatchResult] = None,
    ) -> None:
        values = {}

        if match_time is not None:
            values["match_time"] = match_time.isoformat()

        if local_team is not None:
            values["local_team"] = local_team.value

        if visitor_team is not None:
            values["visitor_team"] = visitor_team.value

        if result is not None:
            values["result"] = result.serialize()

        print(values)

        if values:
            url = f"{self._url}?id=eq.{str(match_id.value)}"
            print(url)
            result = requests.patch(url=url, headers=self._auth_header, data=values)

            if result.status_code != 204:
                raise SupabaseException(result.text)
