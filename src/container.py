from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    DependenciesContainer,
    Provider,
    Factory,
    Container,
)

from core.application.app.fetch_data_service import FetchDataService
from core.application.match.match_list_service import MatchListService
from core.application.ranking.ranking_list_service import RankingListService
from core.application.response.response_creator_service import ResponseCreatorService
from core.application.user.user_creator_service import UserCreatorService
from core.application.user.user_has_answered_updater_service import UserHasNasweredUpdaterService
from core.application.user.user_login_service import UserLoginService
from infrastructure.supabase.container import SupabaseContainer


class Services(DeclarativeContainer):
    database_container = DependenciesContainer()

    user_creator_service: Provider[UserCreatorService] = Factory(
        UserCreatorService,
        user_repository=database_container.user_repository,
    )
    user_login_service: Provider[UserLoginService] = Factory(
        UserLoginService,
        user_repository=database_container.user_repository,
    )
    user_has_answered_updater_service: Provider[UserHasNasweredUpdaterService] = Factory(
        UserHasNasweredUpdaterService,
        user_repository=database_container.user_repository,
    )

    match_list_service: Provider[MatchListService] = Factory(
        MatchListService,
        match_repository=database_container.match_repository,
    )

    response_creator_service: Provider[ResponseCreatorService] = Factory(
        ResponseCreatorService,
        response_repository=database_container.response_repository,
    )

    ranking_list_service: Provider[RankingListService] = Factory(
        RankingListService,
        ranking_repository=database_container.ranking_repository,
    )

    fetch_data_service: Provider[FetchDataService] = Factory(
        FetchDataService,
        match_list_service=match_list_service,
        ranking_list_service=ranking_list_service,
    )


class MainContainer(DeclarativeContainer):
    database_container = Container(SupabaseContainer)

    services = Container(
        Services,
        database_container=database_container,
    )
