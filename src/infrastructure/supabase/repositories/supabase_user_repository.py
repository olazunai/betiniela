from typing import Optional

from supabase import Client

from core.domain.entities.user import User, UserID
from core.domain.repositories.user_repository import UserRepository


class SupabaseUserRepository(UserRepository):
    client: Client
    table: str = "users"

    async def add(self, user: User) -> None:
        self.client.table(self.table).insert(user.serialize()).execute()

    async def get_by_id(self, user_id: UserID) -> Optional[User]:
        result = (
            self.client.table(self.table).select("*").eq("id", user_id.value).execute()
        )

        if not result["data"]:
            return None

        return User.deserialize(result["data"][0])

    async def get(self) -> list[User]:
        query = self.client.table(self.table).select("*")

        result = query.execute()
        return [User.deserialize(data) for data in result["data"]]
