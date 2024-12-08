from dataclasses import dataclass
from datetime import time
from threading import local
from typing import Optional

from supabase import Client

from core.domain.entities.match import Match, MatchID, MatchResult
from core.domain.repositories.match_repository import MatchRepository
from core.domain.value_objects.team import Team
from core.domain.value_objects.week import Week


@dataclass
class SupabaseMatchRepository(MatchRepository):
    client: Client
    table: str = "matches"

    def add(self, match: Match) -> None:
        self.client.table(self.table).insert(match.serialize()).execute()

    def get_by_id(self, match_id: MatchID) -> Optional[Match]:
        result = (
            self.client.table(self.table)
            .select("*")
            .eq("id", str(match_id.value))
            .execute()
        )

        if not result.data:
            return None

        return Match.deserialize(result.data[0])

    def delete(self, match_id: MatchID) -> None:
        self.client.table(self.table).delete().eq("id", str(match_id.value)).execute()

    def get(self, week: Week = None) -> list[Match]:
        query = self.client.table(self.table).select("*")

        if week is not None:
            query = query.eq("week", week.serialize())

        result = (
            query.order("match_day", desc=False)
            .order("match_time", desc=False)
            .execute()
        )
        return [Match.deserialize(data) for data in result.data]

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

        if values:
            self.client.table(self.table).update(values).eq(
                "id", str(match_id.value)
            ).execute()
