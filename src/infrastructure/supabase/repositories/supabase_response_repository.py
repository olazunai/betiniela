from dataclasses import dataclass
from typing import Optional

from supabase import Client

from core.domain.entities.match import MatchID
from core.domain.entities.response import Response, ResponseID
from core.domain.entities.user import UserID
from core.domain.value_objects.week import Week


@dataclass
class ResponseRepository:
    client: Client
    table: str = "responses"

    async def add(self, response: Response) -> None:
        self.client.table(self.table).insert(response.serialize()).execute()

    async def get_by_id(self, response_id: ResponseID) -> Optional[Response]:
        result = (
            self.client.table(self.table)
            .select("*")
            .eq("id", response_id.value)
            .execute()
        )

        if not result["data"]:
            return None

        return Response.deserialize(result["data"][0])

    async def get(
        self, week: Week = None, match_id: MatchID = None, user_id: UserID = None
    ) -> list[Response]:
        query = self.client.table(self.table).select("*")

        if week is not None:
            query = query.eq("week", week.name())

        if match_id is not None:
            query = query.eq("match_id", match_id.value)

        if user_id is not None:
            query = query.eq("user_id", user_id.value)

        result = query.execute()
        return [Response.deserialize(data) for data in result["data"]]

    async def update(self, response: Response) -> None:
        self.client.table(self.table).upsert(response.serialize()).execute()
