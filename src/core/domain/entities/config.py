from dataclasses import dataclass

from src.core.domain.value_objects.week import Week


@dataclass
class Config:
    current_week: Week
    right_winner_points: int
    right_losser_points: int
    started_week: bool

    def serialize(self) -> dict:
        return {
            "current_week": self.current_week.serialize(),
            "right_winner_points": self.right_winner_points,
            "right_losser_points": self.right_losser_points,
            "started_week": self.started_week,
        }

    @classmethod
    def deserialize(cls, obj: dict) -> "Config":
        return cls(
            current_week=Week.deserialize(obj["current_week"]),
            right_winner_points=int(obj["right_winner_points"]),
            right_losser_points=int(obj["right_losser_points"]),
            started_week=obj["started_week"],
        )
