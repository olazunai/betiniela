from abc import ABC, abstractmethod
from typing import Optional

from core.domain.entities.match import Match, MatchID, MatchResult
from core.domain.value_objects.week import Week


class MatchRepository(ABC):
    @abstractmethod
    async def add(self, match: Match) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, match_id: MatchID) -> Optional[Match]:
        pass

    @abstractmethod
    async def get(self, week: Week = None) -> list[Match]:
        pass

    @abstractmethod
    async def update_result(self, match_id: MatchID, result: MatchResult) -> None:
        pass
