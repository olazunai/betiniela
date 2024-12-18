from dataclasses import dataclass

from src.core.application.user.user_list_service import UserListService
from src.core.application.config.config_retriever_service import ConfigRetrieverService
from src.core.application.match.match_list_service import MatchListService
from src.core.application.ranking.ranking_list_service import RankingListService
from src.core.application.response.response_list_service import ResponseListService
from src.core.domain.dtos.data import Data


@dataclass
class FetchDataService:
    match_list_service: MatchListService
    ranking_list_service: RankingListService
    response_list_service: ResponseListService
    config_retriever_service: ConfigRetrieverService
    user_list_service: UserListService

    def __call__(self) -> Data:
        matches_by_week = self.match_list_service()
        rankings = self.ranking_list_service()
        responses_by_week = self.response_list_service()
        config = self.config_retriever_service()
        users = self.user_list_service()

        return Data(
            matches_by_week=matches_by_week,
            responses_by_week=responses_by_week,
            rankings=rankings,
            config=config,
            users=users,
        )
