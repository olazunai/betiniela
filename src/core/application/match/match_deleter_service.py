from dataclasses import dataclass
from uuid import UUID

from src.core.domain.entities.match import MatchID
from src.core.domain.exceptions import MatchDoesNotExistException
from src.core.domain.repositories.match_repository import MatchRepository


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
