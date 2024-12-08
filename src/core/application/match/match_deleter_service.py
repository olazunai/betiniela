from dataclasses import dataclass
from uuid import UUID

from core.domain.entities.match import MatchID
from core.domain.exceptions import MatchDoesNotExistException
from core.domain.repositories.match_repository import MatchRepository
from core.domain.value_objects.team import Team


@dataclass
class MatchDeleterService:
    match_repository: MatchRepository

    def __call__(self, match_id: UUID) -> None:
        match = self.match_repository.get_by_id(match_id=MatchID(match_id))
        if match is None:
            raise MatchDoesNotExistException(
                f"Trying to delete a match {match_id} that does not exist"
            )
        self.match_repository.delete(
            match_id=MatchID(match_id),
        )
