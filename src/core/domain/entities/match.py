from datetime import date, time
from typing import Optional
from uuid import UUID
from attr import dataclass

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
