from uuid import UUID
from dataclasses import dataclass

from core.domain.entities.user import UserID
from core.domain.value_objects.week import Week


@dataclass
class RankingID:
    value: UUID


@dataclass
class RankingPosition:
    value: int


@dataclass
class RankingPoints:
    value: int


@dataclass
class Ranking:
    id: RankingID
    week: Week
    user_id: UserID
    position: RankingPosition
    points: RankingPoints

    def serialize(self) -> dict:
        return {
            "id": self.id.value,
            "week": self.week.name(),
            "user_id": self.user_id.value,
            "position": self.position.value,
            "points": self.points.value,
        }

    @classmethod
    def deserialize(cls, obj: dict) -> "Ranking":
        return cls(
            id=UUID(obj["id"]),
            week=Week.deserialize(obj["week"]),
            user_id=UserID(obj["user_id"]),
            position=RankingPosition(obj["position"]),
            points=RankingPoints(obj["points"]),
        )
