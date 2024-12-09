from dataclasses import dataclass

from src.core.domain.entities.ranking import Ranking
from src.core.domain.repositories.ranking_repository import RankingRepository
from src.core.domain.value_objects.week import Week


@dataclass
class RankingListService:
    ranking_repository: RankingRepository

    def __call__(self, week_name: str) -> list[Ranking]:
        rankings = self.ranking_repository.get(Week.deserialize(week_name))

        return rankings
