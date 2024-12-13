from env import SUPABASE_KEY, SUPABASE_URL
from src.core.application.app.auth_service import AuthService
from src.core.application.app.calculate_points_service import CalculatePointService
from src.core.application.app.fetch_data_service import FetchDataService
from src.core.application.config.config_retriever_service import ConfigRetrieverService
from src.core.application.config.config_updater_service import ConfigUpdaterService
from src.core.application.match.match_creator_service import MatchCreatorService
from src.core.application.match.match_deleter_service import MatchDeleterService
from src.core.application.match.match_list_service import MatchListService
from src.core.application.match.match_updater_service import (
    MatchUpdaterService,
)
from src.core.application.ranking.ranking_list_service import RankingListService
from src.core.application.response.response_creator_service import (
    ResponseCreatorService,
)
from src.core.application.response.response_list_service import ResponseListService
from src.core.application.response.response_updater_service import (
    ResponseUpdaterService,
)
from src.core.application.user.user_creator_service import UserCreatorService
from src.core.application.user.user_has_answered_updater_service import (
    UserHasNasweredUpdaterService,
)
from src.core.application.user.user_login_service import UserLoginService
from src.core.application.user.user_retriever_service import UserRetrieverService
from src.infrastructure.supabase.container import SupabaseContainer


class Services:
    def __init__(self, database_container: SupabaseContainer):
        self.user_creator_service = UserCreatorService(
            user_repository=database_container.user_repository,
        )
        self.user_login_service = UserLoginService(
            user_repository=database_container.user_repository,
        )
        self.user_has_answered_updater_service = UserHasNasweredUpdaterService(
            user_repository=database_container.user_repository,
        )
        self.user_retriever_service = UserRetrieverService(
            user_repository=database_container.user_repository,
        )

        self.match_list_service = MatchListService(
            match_repository=database_container.match_repository,
        )
        self.match_updater_service = MatchUpdaterService(
            match_repository=database_container.match_repository,
        )
        self.match_deleter_service = MatchDeleterService(
            match_repository=database_container.match_repository,
        )
        self.match_creator_service = MatchCreatorService(
            match_repository=database_container.match_repository,
        )

        self.response_creator_service = ResponseCreatorService(
            response_repository=database_container.response_repository,
        )
        self.response_list_service = ResponseListService(
            response_repository=database_container.response_repository,
        )
        self.response_updater_service = ResponseUpdaterService(
            response_repository=database_container.response_repository,
        )

        self.ranking_list_service = RankingListService(
            ranking_repository=database_container.ranking_repository,
        )

        self.config_retriever_service = ConfigRetrieverService(
            config_repository=database_container.config_repository,
        )
        self.config_updater_service = ConfigUpdaterService(
            config_repository=database_container.config_repository,
        )

        self.fetch_data_service = FetchDataService(
            match_list_service=self.match_list_service,
            ranking_list_service=self.ranking_list_service,
            response_list_service=self.response_list_service,
            config_retriever_service=self.config_retriever_service,
        )
        self.auth_service = AuthService(
            user_login_service=self.user_login_service,
        )
        self.calculate_points_service = CalculatePointService(
            config_repository=database_container.config_repository,
            response_repository=database_container.response_repository,
            ranking_repository=database_container.ranking_repository,
            match_repository=database_container.match_repository,
            user_repository=database_container.user_repository,
        )


class MainContainer:
    def __init__(self):
        self.database_container = SupabaseContainer(url=SUPABASE_URL, key=SUPABASE_KEY)

        self.services = Services(
            database_container=self.database_container,
        )
