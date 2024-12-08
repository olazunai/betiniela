from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    DependenciesContainer,
    Provider,
    Factory,
    Container,
    Configuration,
)

from core.application.app.auth_service import AuthService
from core.application.app.calculate_points_service import CalculatePointService
from core.application.app.fetch_data_service import FetchDataService
from core.application.config.config_retriever_service import ConfigRetrieverService
from core.application.config.config_updater_service import ConfigUpdaterService
from core.application.match.match_creator_service import MatchCreatorService
from core.application.match.match_deleter_service import MatchDeleterService
from core.application.match.match_list_service import MatchListService
from core.application.match.match_updater_service import (
    MatchUpdaterService,
)
from core.application.ranking.ranking_list_service import RankingListService
from core.application.response.response_creator_service import ResponseCreatorService
from core.application.response.response_list_service import ResponseListService
from core.application.response.response_updater_service import ResponseUpdaterService
from core.application.user.user_creator_service import UserCreatorService
from core.application.user.user_has_answered_updater_service import (
    UserHasNasweredUpdaterService,
)
from core.application.user.user_login_service import UserLoginService
from infrastructure.supabase.container import SupabaseContainer


class Services(DeclarativeContainer):
    config = Configuration()
    config.secret_key.from_env("SECRET_KEY", "")

    database_container = DependenciesContainer()

    user_creator_service: Provider[UserCreatorService] = Factory(
        UserCreatorService,
        user_repository=database_container.user_repository,
    )
    user_login_service: Provider[UserLoginService] = Factory(
        UserLoginService,
        user_repository=database_container.user_repository,
    )
    user_has_answered_updater_service: Provider[UserHasNasweredUpdaterService] = (
        Factory(
            UserHasNasweredUpdaterService,
            user_repository=database_container.user_repository,
        )
    )

    match_list_service: Provider[MatchListService] = Factory(
        MatchListService,
        match_repository=database_container.match_repository,
    )
    match_updater_service: Provider[MatchUpdaterService] = Factory(
        MatchUpdaterService,
        match_repository=database_container.match_repository,
    )
    match_deleter_service: Provider[MatchDeleterService] = Factory(
        MatchDeleterService,
        match_repository=database_container.match_repository,
    )
    match_creator_service: Provider[MatchCreatorService] = Factory(
        MatchCreatorService,
        match_repository=database_container.match_repository,
    )

    response_creator_service: Provider[ResponseCreatorService] = Factory(
        ResponseCreatorService,
        response_repository=database_container.response_repository,
    )
    response_list_service: Provider[ResponseListService] = Factory(
        ResponseListService,
        response_repository=database_container.response_repository,
    )
    response_updater_service: Provider[ResponseUpdaterService] = Factory(
        ResponseUpdaterService,
        response_repository=database_container.response_repository,
    )

    ranking_list_service: Provider[RankingListService] = Factory(
        RankingListService,
        ranking_repository=database_container.ranking_repository,
    )

    config_retriever_service: Provider[ConfigRetrieverService] = Factory(
        ConfigRetrieverService,
        config_repository=database_container.config_repository,
    )
    config_updater_service: Provider[ConfigUpdaterService] = Factory(
        ConfigUpdaterService,
        config_repository=database_container.config_repository,
    )

    fetch_data_service: Provider[FetchDataService] = Factory(
        FetchDataService,
        match_list_service=match_list_service,
        ranking_list_service=ranking_list_service,
        response_list_service=response_list_service,
        config_retriever_service=config_retriever_service,
    )
    auth_service: Provider[AuthService] = Factory(
        AuthService,
        user_login_service=user_login_service,
        secret_key=config.secret_key,
    )
    calculate_points_service: Provider[CalculatePointService] = Factory(
        CalculatePointService,
        config_repository=database_container.config_repository,
        response_repository=database_container.response_repository,
        ranking_repository=database_container.ranking_repository,
        match_repository=database_container.match_repository,
        user_repository=database_container.user_repository,
    )


class MainContainer(DeclarativeContainer):
    database_container = Container(SupabaseContainer)

    services = Container(
        Services,
        database_container=database_container,
    )
