from dataclasses import dataclass

from core.domain.entities.ranking import Ranking
from core.domain.repositories.ranking_repository import RankingRepository
from core.domain.value_objects.week import Week


@dataclass
class RankingListService:
    ranking_repository: RankingRepository

    async def __call__(self, week_name: str) -> list[Ranking]:
        rankings = await self.ranking_repository.get(Week.deserialize(week_name))

        return rankings
