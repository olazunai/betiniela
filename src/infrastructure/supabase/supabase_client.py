from dataclasses import dataclass
from typing import Optional
from src.core.domain.interfaces.bbdd_client import BBDDClient
from supabase import create_client, Client


@dataclass
class SupabaseClient(BBDDClient):
    client: Optional[Client] = None

    @classmethod
    def init(cls, url: str, key: str) -> "SupabaseClient":
        return cls(
            client=create_client(
                supabase_url=url,
                supabase_key=key,
            ),
        )

    def close(self) -> None:
        pass
