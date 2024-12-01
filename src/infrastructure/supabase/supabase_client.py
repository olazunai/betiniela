from dataclasses import dataclass
from typing import Optional
from core.domain.interfaces.bbdd_client import BBDDClient
from supabase import create_client, Client


@dataclass
class SupabaseClient(BBDDClient):
    client: Optional[Client] = None

    @classmethod
    def init(self, url: str, key: str) -> "SupabaseClient":
        self.client: Client = create_client(
            supabase_url=url,
            supabase_key=key,
        )

    def close(self) -> None:
        pass
