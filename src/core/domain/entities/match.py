from datetime import date, time
import json
from typing import Optional, Union
from uuid import UUID
from dataclasses import dataclass

from src.core.domain.value_objects.team import Team
from src.core.domain.value_objects.week import Week


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
        return json.dumps(
            {
                "local_team": self.local_team,
                "visitor_team": self.visitor_team,
            },
        )

    @classmethod
    def deserialize(cls, obj: Union[str, dict]) -> "MatchResult":
        if isinstance(obj, str):
            obj = json.loads(obj)
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
    match_time: time = None
    result: Optional[MatchResult] = None

    def serialize(self) -> dict:
        return {
            "id": str(self.id.value),
            "week": self.week.serialize(),
            "match_day": self.match_day.isoformat(),
            "local_team": self.local_team.value,
            "visitor_team": self.visitor_team.value,
            "location": self.location.value,
            "match_time": self.match_time.isoformat(),
            "result": self.result.serialize() if self.result is not None else None,
        }

    @classmethod
    def deserialize(cls, obj: dict) -> "Match":
        return cls(
            id=MatchID(UUID(obj["id"])),
            week=Week.deserialize(obj["week"]),
            match_day=date.fromisoformat(obj["match_day"]),
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
