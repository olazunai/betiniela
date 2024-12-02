from dataclasses import dataclass

from core.application.match.match_list_service import MatchListService
from core.application.ranking.ranking_list_service import RankingListService
from core.domain.dtos.data import Data
from core.domain.entities.match import Match


@dataclass
class FetchDataService:
    match_list_service: MatchListService
    ranking_list_service: RankingListService

    async def __call__(self) -> Data:
        matches_by_week = await self.match_list_service()
        rankings = await self.ranking_list_service(week_name="jornada 1")

        return Data(
            matches_by_week=matches_by_week,
            rankings=rankings,
        )
