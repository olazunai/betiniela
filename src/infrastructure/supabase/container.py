from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Provider, Configuration, Resource
from dependency_injector import resources
from supabase import Client, create_client

from core.domain.repositories.match_repository import MatchRepository
from core.domain.repositories.ranking_repository import RankingRepository
from core.domain.repositories.response_repository import ResponseRepository
from core.domain.repositories.user_repository import UserRepository
from infrastructure.supabase.repositories.supabase_match_repository import (
    SupabaseMatchRepository,
)
from infrastructure.supabase.repositories.supabase_ranking_repository import (
    SupabaseRankingRepository,
)
from infrastructure.supabase.repositories.supabase_response_repository import (
    SupabaseResponseRepository,
)
from infrastructure.supabase.repositories.supabase_user_repository import (
    SupabaseUserRepository,
)


class ConfigureSupabaseClient(resources.Resource):
    def init(self, url: str, key: str) -> Client:
        return create_client(
            supabase_url=url,
            supabase_key=key,
        )

    def shutdown(self, client: Client) -> None:
        pass


class SupabaseContainer(DeclarativeContainer):
    config = Configuration()
    config.url.from_env("SUPABASE_URL", "")
    config.key.from_env("SUPABASE_KEY", "")

    client = Resource(
        ConfigureSupabaseClient,
        url=config.url,
        key=config.key,
    )

    user_repository: Provider[UserRepository] = Singleton(
        SupabaseUserRepository,
        client=client,
    )
    match_repository: Provider[MatchRepository] = Singleton(
        SupabaseMatchRepository,
        client=client,
    )
    ranking_repository: Provider[RankingRepository] = Singleton(
        SupabaseRankingRepository,
        client=client,
    )
    response_repository: Provider[ResponseRepository] = Singleton(
        SupabaseResponseRepository,
        client=client,
    )
