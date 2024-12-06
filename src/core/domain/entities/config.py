from dataclasses import dataclass
from datetime import datetime

from core.domain.value_objects.week import Week


@dataclass
class Config:
    current_week: Week
    betting_limit: datetime
    right_winner_points: int
    right_losser_points: int

    def serialize(self) -> dict:
        return {
            "current_week": self.current_week.serialize(),
            "betting_limit": self.betting_limit.isoformat(),
            "right_winner_points": self.right_winner_points,
            "right_losser_points": self.right_losser_points,
        }

    @classmethod
    def deserialize(cls, obj: dict) -> "Config":
        return cls(
            current_week=Week.deserialize(obj["current_week"]),
            betting_limit=datetime.fromisoformat(obj["betting_limit"]),
            right_winner_points=int(obj["right_winner_points"]),
            right_losser_points=int(obj["right_losser_points"]),
        )
