from abc import ABC, abstractmethod
from typing import Optional

from src.core.domain.entities.ranking import Ranking, RankingID, RankingPoints
from src.core.domain.entities.user import UserName
from src.core.domain.value_objects.week import Week


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
    def get(self, week: Week = None, user_name: UserName = None) -> list[Ranking]:
        pass

    @abstractmethod
    def update_points(self, ranking_id: RankingID, points: RankingPoints) -> None:
        pass
