import os

from src.core.domain.repositories.config_repository import ConfigRepository
from src.core.domain.repositories.match_repository import MatchRepository
from src.core.domain.repositories.ranking_repository import RankingRepository
from src.core.domain.repositories.response_repository import ResponseRepository
from src.core.domain.repositories.user_repository import UserRepository
from src.infrastructure.supabase.repositories.supabase_config_repository import (
    SupabaseConfigRepository,
)
from src.infrastructure.supabase.repositories.supabase_match_repository import (
    SupabaseMatchRepository,
)
from src.infrastructure.supabase.repositories.supabase_ranking_repository import (
    SupabaseRankingRepository,
)
from src.infrastructure.supabase.repositories.supabase_response_repository import (
    SupabaseResponseRepository,
)
from src.infrastructure.supabase.repositories.supabase_user_repository import (
    SupabaseUserRepository,
)


class SupabaseContainer:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL", "")
        self.key = os.getenv("SUPABASE_KEY", "")

        self.user_repository: UserRepository = SupabaseUserRepository(
            base_url=self.url,
            api_key=self.key,
        )
        self.match_repository: MatchRepository = SupabaseMatchRepository(
            base_url=self.url,
            api_key=self.key,
        )
        self.ranking_repository: RankingRepository = SupabaseRankingRepository(
            base_url=self.url,
            api_key=self.key,
        )
        self.response_repository: ResponseRepository = SupabaseResponseRepository(
            base_url=self.url,
            api_key=self.key,
        )
        self.config_repository: ConfigRepository = SupabaseConfigRepository(
            base_url=self.url,
            api_key=self.key,
        )
