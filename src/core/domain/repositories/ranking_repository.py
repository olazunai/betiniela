from abc import ABC, abstractmethod
from typing import Optional

from core.domain.entities.ranking import Ranking, RankingID, RankingPoints
from core.domain.entities.user import UserID
from core.domain.value_objects.week import Week


class RankingRepository(ABC):
    @abstractmethod
    def add(self, ranking: Ranking) -> None:
        pass

    @abstractmethod
    def add_or_update(self, ranking: Ranking) -> None:
        pass

    @abstractmethod
    def get_by_id(self, ranking_id: RankingID) -> Optional[Ranking]:
        pass

    @abstractmethod
    def get(self, week: Week = None, user_id: UserID = None) -> list[Ranking]:
        pass

    @abstractmethod
    def update_points(self, ranking_id: RankingID, points: RankingPoints) -> None:
        pass
