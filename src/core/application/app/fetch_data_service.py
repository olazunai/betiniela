from dataclasses import dataclass

from core.application.match.match_list_service import MatchListService
from core.domain.dtos.data import Data
from core.domain.entities.match import Match


@dataclass
class FetchDataService:
    match_list_service: MatchListService

    async def __call__(self) -> Data:
        matches_by_week = await self.match_list_service()

        return Data(matches_by_week=matches_by_week)
