from dataclasses import dataclass
from datetime import time
from typing import Optional
from uuid import UUID

from src.core.domain.entities.match import MatchID, MatchResult
from src.core.domain.repositories.match_repository import MatchRepository
from src.core.domain.value_objects.team import Team


@dataclass
class MatchUpdaterService:
    match_repository: MatchRepository

    def __call__(
        self,
        match_id: UUID,
        match_time: Optional[time] = None,
        local_team: Optional[str] = None,
        visitor_team: Optional[str] = None,
        local_team_result: Optional[int] = None,
        visitor_team_result: Optional[int] = None,
    ) -> None:
        result = None
        if local_team_result is not None and visitor_team_result is not None:
            result = MatchResult(
                local_team=local_team_result,
                visitor_team=visitor_team_result,
            )

        self.match_repository.update(
            match_id=MatchID(match_id),
            match_time=match_time,
            local_team=Team(local_team) if local_team is not None else None,
            visitor_team=Team(visitor_team) if visitor_team is not None else None,
            result=result,
        )
