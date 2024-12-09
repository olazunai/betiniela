from dataclasses import dataclass
from typing import Optional

from supabase import Client

from src.core.domain.entities.ranking import Ranking, RankingID, RankingPoints
from src.core.domain.entities.user import UserID
from src.core.domain.repositories.ranking_repository import RankingRepository
from src.core.domain.value_objects.week import Week


@dataclass
class SupabaseRankingRepository(RankingRepository):
    client: Client
    table: str = "rankings"

    def add(self, ranking: Ranking) -> None:
        self.client.table(self.table).insert(ranking.serialize()).execute()

    def add_or_update(self, ranking: Ranking) -> None:
        self.client.table(self.table).upsert(ranking.serialize()).execute()

    def get_by_id(self, ranking_id: RankingID) -> Optional[Ranking]:
        result = (
            self.client.table(self.table)
            .select("*")
            .eq("id", str(ranking_id.value))
            .execute()
        )

        if not result.data:
            return None

        return Ranking.deserialize(result.data[0])

    def get(self, week: Week = None, user_id: UserID = None) -> list[Ranking]:
        query = self.client.table(self.table).select("*")

        if week is not None:
            query = query.eq("week", week.serialize())

        if user_id is not None:
            query = query.eq("user_id", str(user_id.value))

        result = query.order("points", desc=True).execute()
        return [Ranking.deserialize(data) for data in result.data]

    def update_points(self, ranking_id: RankingID, points: RankingPoints) -> None:
        self.client.table(self.table).update({"points": points.value}).eq(
            "id", str(ranking_id.value)
        ).execute()
