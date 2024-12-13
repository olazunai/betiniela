from datetime import datetime
from enum import StrEnum
from typing import Optional
from uuid import UUID
from dataclasses import dataclass

from src.core.domain.entities.match import MatchID
from src.core.domain.entities.user import UserID, UserName
from src.core.domain.value_objects.team import Team
from src.core.domain.value_objects.week import Week


@dataclass
class ResponseID:
    value: UUID


class ResponseLosserPoints(StrEnum):
    VERY_FEW = "0-6"
    FEW = "7-11"
    NORMAL = "12-15"
    MANY = "16-18"
    VERY_MANY = "19-21"

    def contains(self, value: int) -> bool:
        interval = self.value.split("-")
        return value >= int(interval[0]) and value <= int(interval[1])


@dataclass
class Response:
    id: ResponseID
    week: Week
    match_id: MatchID
    user_id: UserID
    user_name: UserName
    winner: Team
    losser_points: ResponseLosserPoints
    response_time: datetime
    updated_time: Optional[datetime] = None

    def serialize(self) -> dict:
        return {
            "id": str(self.id.value),
            "week": self.week.serialize(),
            "match_id": str(self.match_id.value),
            "user_id": str(self.user_id.value),
            "user_name": self.user_name.value,
            "winner": self.winner.value,
            "losser_points": self.losser_points.value,
            "response_time": self.response_time.isoformat(),
            "updated_time": (
                self.updated_time.isoformat() if self.updated_time is not None else None
            ),
        }

    @classmethod
    def deserialize(cls, obj: dict) -> "Response":
        return cls(
            id=ResponseID(UUID(obj["id"])),
            week=Week.deserialize(obj["week"]),
            match_id=MatchID(UUID(obj["match_id"])),
            user_id=UserID(UUID(obj["user_id"])),
            user_name=UserName(obj["user_name"]),
            winner=Team(obj["winner"]),
            losser_points=ResponseLosserPoints(obj["losser_points"]),
            response_time=datetime.fromisoformat(obj["response_time"]),
            updated_time=(
                datetime.fromisoformat(obj["updated_time"])
                if obj.get("updated_time") is not None
                else None
            ),
        )
