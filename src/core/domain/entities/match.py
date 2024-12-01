from datetime import date, time
from typing import Optional
from uuid import UUID
from dataclasses import dataclass

from core.domain.value_objects.team import Team
from core.domain.value_objects.week import Week


@dataclass
class MatchID:
    value: UUID


@dataclass
class MatchLocation:
    value: str


@dataclass
class MatchResult:
    local_team: int
    visitor_team: int

    def serialize(self):
        return {
            "local_team": self.local_team,
            "visitor_team": self.visitor_team,
        }

    @classmethod
    def deserialize(cls, obj: dict) -> "MatchResult":
        return cls(
            local_team=obj["local_team"],
            visitor_team=obj["visitor_team"],
        )


@dataclass
class Match:
    id: MatchID
    week: Week
    match_day: date
    local_team: Team
    visitor_team: Team
    location: MatchLocation
    match_time: Optional[time] = None
    result: Optional[MatchResult] = None

    def serialize(self) -> dict:
        return {
            "id": self.id.value,
            "week": self.week.name(),
            "match_day": self.match_day.isoformat(),
            "local_team": self.local_team.value,
            "visitor_team": self.visitor_team.value,
            "location": self.location.value,
            "match_time": (
                self.match_time.isoformat() if self.match_time is not None else None
            ),
            "result": self.result.serialize() if self.result is not None else None,
        }

    @classmethod
    def deserialize(cls, obj: dict) -> "Match":
        return cls(
            id=UUID(obj["id"]),
            week=Week.deserialize(obj["week"]),
            match_day=date.fromisoformat(obj["date"]),
            local_team=Team(obj["local_team"]),
            visitor_team=Team(obj["visitor_team"]),
            location=MatchLocation(obj["location"]),
            match_time=(
                time.fromisoformat(obj["match_time"])
                if obj.get("match_time") is not None
                else None
            ),
            result=(
                MatchResult.deserialize(obj["result"])
                if obj.get("result") is not None
                else None
            ),
        )
