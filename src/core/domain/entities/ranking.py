from uuid import UUID
from dataclasses import dataclass

from core.domain.entities.user import UserID, UserName
from core.domain.value_objects.week import Week


@dataclass
class RankingID:
    value: UUID


@dataclass
class RankingPoints:
    value: int


@dataclass
class Ranking:
    id: RankingID
    user_name: UserName
    week: Week
    points: RankingPoints

    def serialize(self) -> dict:
        return {
            "id": str(self.id.value),
            "week": self.week.name(),
            "user_name": self.user_name.value,
            "points": self.points.value,
        }

    @classmethod
    def deserialize(cls, obj: dict) -> "Ranking":
        return cls(
            id=RankingID(UUID(obj["id"])),
            week=Week.deserialize(obj["week"]),
            user_name=UserName(obj["user_name"]),
            points=RankingPoints(obj["points"]),
        )
