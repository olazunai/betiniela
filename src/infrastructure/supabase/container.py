import os
from supabase import Client, create_client

from core.domain.repositories.config_repository import ConfigRepository
from core.domain.repositories.match_repository import MatchRepository
from core.domain.repositories.ranking_repository import RankingRepository
from core.domain.repositories.response_repository import ResponseRepository
from core.domain.repositories.user_repository import UserRepository
from infrastructure.supabase.repositories.supabase_config_repository import (
    SupabaseConfigRepository,
)
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


class ConfigureSupabaseClient:
    @staticmethod
    def init(url: str, key: str) -> Client:
        return create_client(
            supabase_url=url,
            supabase_key=key,
        )

    @staticmethod
    def shutdown(client: Client) -> None:
        pass


class SupabaseContainer:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL", "")
        self.key = os.getenv("SUPABASE_KEY", "")

        self.client: Client = ConfigureSupabaseClient.init(
            url=self.url,
            key=self.key,
        )

        self.user_repository: UserRepository = SupabaseUserRepository(
            client=self.client,
        )
        self.match_repository: MatchRepository = SupabaseMatchRepository(
            client=self.client,
        )
        self.ranking_repository: RankingRepository = SupabaseRankingRepository(
            client=self.client,
        )
        self.response_repository: ResponseRepository = SupabaseResponseRepository(
            client=self.client,
        )
        self.config_repository: ConfigRepository = SupabaseConfigRepository(
            client=self.client,
        )

    def shutdown(self) -> None:
        ConfigureSupabaseClient.shutdown(self.client)
