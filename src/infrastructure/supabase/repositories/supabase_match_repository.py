from dataclasses import dataclass
from typing import Optional

from supabase import Client

from core.domain.entities.match import Match, MatchID, MatchResult
from core.domain.repositories.match_repository import MatchRepository
from core.domain.value_objects.week import Week


@dataclass
class SupabaseMatchRepository(MatchRepository):
    client: Client
    table: str = "matches"

    async def add(self, match: Match) -> None:
        self.client.table(self.table).insert(match.serialize()).execute()

    async def get_by_id(self, match_id: MatchID) -> Optional[Match]:
        result = (
            self.client.table(self.table).select("*").eq("id", match_id.value).execute()
        )

        if not result["data"]:
            return None

        return Match.deserialize(result["data"][0])

    async def get(self, week: Week = None) -> list[Match]:
        query = self.client.table(self.table).select("*")

        if week is not None:
            query = query.eq("week", week.name())

        result = query.execute()
        return [Match.deserialize(data) for data in result["data"]]

    async def update_result(self, match_id: MatchID, result: MatchResult) -> None:
        self.client.table(self.table).update("result", result.serialize()).eq(
            "id", match_id.value
        ).execute()
