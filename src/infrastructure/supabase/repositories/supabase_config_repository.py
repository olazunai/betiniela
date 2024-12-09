from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from supabase import Client

from src.core.domain.entities.config import Config
from src.core.domain.repositories.config_repository import ConfigRepository
from src.core.domain.value_objects.week import Week


@dataclass
class SupabaseConfigRepository(ConfigRepository):
    client: Client
    table: str = "configuration"

    def get(self) -> Config:
        result = self.client.table(self.table).select("*").execute()

        return Config.deserialize(result.data[0])

    def update(
        self,
        current_week: Optional[Week] = None,
        betting_limit: Optional[datetime] = None,
        right_winner_points: Optional[int] = None,
        right_losser_points: Optional[int] = None,
    ) -> None:
        result = self.client.table(self.table).select("id").execute()

        config_id = result.data[0]["id"]

        values = {}

        if current_week is not None:
            values["current_week"] = current_week.serialize()

        if betting_limit is not None:
            values["betting_limit"] = betting_limit.isoformat()

        if right_winner_points is not None:
            values["right_winner_points"] = right_winner_points

        if right_losser_points is not None:
            values["right_losser_points"] = right_losser_points

        if values:
            self.client.table(self.table).update(values).eq("id", config_id).execute()
