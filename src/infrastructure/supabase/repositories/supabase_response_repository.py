from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from supabase import Client

from src.core.domain.entities.match import MatchID
from src.core.domain.entities.response import Response, ResponseID, ResponseLosserPoints
from src.core.domain.entities.user import UserID
from src.core.domain.value_objects.team import Team
from src.core.domain.value_objects.week import Week


@dataclass
class SupabaseResponseRepository:
    client: Client
    table: str = "responses"

    def add(self, response: Response) -> None:
        self.client.table(self.table).insert(response.serialize()).execute()

    def get_by_id(self, response_id: ResponseID) -> Optional[Response]:
        result = (
            self.client.table(self.table)
            .select("*")
            .eq("id", str(response_id.value))
            .execute()
        )

        if not result.data:
            return None

        return Response.deserialize(result.data[0])

    def get(
        self, week: Week = None, match_id: MatchID = None, user_id: UserID = None
    ) -> list[Response]:
        query = self.client.table(self.table).select("*")

        if week is not None:
            query = query.eq("week", week.serialize())

        if match_id is not None:
            query = query.eq("match_id", str(match_id.value))

        if user_id is not None:
            query = query.eq("user_id", str(user_id.value))

        result = query.execute()
        return [Response.deserialize(data) for data in result.data]

    def update_data(
        self, response_id: ResponseID, winner: Team, losser_points: ResponseLosserPoints
    ) -> None:
        self.client.table(self.table).update(
            {
                "losser_points": losser_points.value,
                "winner": winner.value,
                "updated_time": datetime.now().isoformat(),
            }
        ).eq("id", str(response_id.value)).execute()
