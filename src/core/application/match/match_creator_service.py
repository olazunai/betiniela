from dataclasses import dataclass
from datetime import time
from uuid import uuid4

from core.domain.entities.match import MatchID, MatchLocation, Match
from core.domain.repositories.match_repository import MatchRepository
from core.domain.value_objects.team import Team
from core.domain.value_objects.week import Week


@dataclass
class MatchCreatorService:
    match_repository: MatchRepository

    def __call__(
        self,
        week: str,
        match_day: str,
        match_time: time,
        local_team: str,
        visitor_team: str,
        location: str,
    ) -> None:

        match = Match(
            id=MatchID(uuid4()),
            week=Week.deserialize(week),
            match_day=match_day,
            local_team=Team(local_team),
            visitor_team=Team(visitor_team),
            location=MatchLocation(location),
            match_time=match_time,
        )

        self.match_repository.add(match)
