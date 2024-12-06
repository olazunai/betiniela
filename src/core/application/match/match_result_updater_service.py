from dataclasses import dataclass
from uuid import UUID

from core.domain.entities.match import MatchID, MatchResult
from core.domain.repositories.match_repository import MatchRepository


@dataclass
class MatchResultUpdaterService:
    match_repository: MatchRepository

    def __call__(self, match_id: UUID, local_team: int, visitor_team: int) -> None:
        result = MatchResult(
            local_team=local_team,
            visitor_team=visitor_team,
        )
        self.match_repository.update_result(match_id=MatchID(match_id), result=result)
