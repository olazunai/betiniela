from abc import ABC, abstractmethod
from datetime import time
from typing import Optional

from src.core.domain.entities.match import Match, MatchID, MatchResult
from src.core.domain.value_objects.team import Team
from src.core.domain.value_objects.week import Week


class MatchRepository(ABC):
    @abstractmethod
    def add(self, match: Match) -> None:
        pass

    @abstractmethod
    def get_by_id(self, match_id: MatchID) -> Optional[Match]:
        pass

    @abstractmethod
    def delete(self, match_id: MatchID) -> None:
        pass

    @abstractmethod
    def get(self, week: Week = None) -> list[Match]:
        pass

    @abstractmethod
    def update(
        self,
        match_id: MatchID,
        match_time: time,
        local_team: Team,
        visitor_team: Team,
        result: MatchResult,
    ) -> None:
        pass
