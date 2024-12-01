from dataclasses import dataclass
from typing import Optional

from supabase import Client

from core.domain.entities.ranking import Ranking, RankingID, RankingPoints
from core.domain.repositories.ranking_repository import RankingRepository
from core.domain.value_objects.week import Week


@dataclass
class SupabaseRankingRepository(RankingRepository):
    client: Client
    table: str = "rankings"

    async def add(self, ranking: Ranking) -> None:
        self.client.table(self.table).insert(ranking.serialize()).execute()

    async def get_by_id(self, ranking_id: RankingID) -> Optional[Ranking]:
        result = (
            self.client.table(self.table)
            .select("*")
            .eq("id", ranking_id.value)
            .execute()
        )

        if not result["data"]:
            return None

        return Ranking.deserialize(result["data"][0])

    async def get(self, week: Week = None) -> list[Ranking]:
        query = self.client.table(self.table).select("*")

        if week is not None:
            query = query.eq("week", week.name())

        result = query.execute()
        return [Ranking.deserialize(data) for data in result["data"]]

    async def update_points(self, ranking_id: RankingID, points: RankingPoints) -> None:
        self.client.table(self.table).update("points", points.value).eq(
            "id", ranking_id.value
        ).execute()
