from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    DependenciesContainer,
    Provider,
    Factory,
    Container,
)

from core.application.user.user_creator_service import UserCreatorService
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


class MainContainer(DeclarativeContainer):
    database_container = Container(SupabaseContainer)

    services = Container(
        Services,
        database_container=database_container,
    )
