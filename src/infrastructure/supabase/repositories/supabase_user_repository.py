from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from supabase import Client

from src.core.domain.entities.user import User, UserHasAnswered, UserID, UserName
from src.core.domain.repositories.user_repository import UserRepository


@dataclass
class SupabaseUserRepository(UserRepository):
    client: Client
    table: str = "users"

    def add(self, user: User) -> None:
        self.client.table(self.table).insert(user.serialize()).execute()

    def get_by_id(self, user_id: UserID) -> Optional[User]:
        result = (
            self.client.table(self.table)
            .select("*")
            .eq("id", str(user_id.value))
            .execute()
        )

        if not result.data:
            return None

        return User.deserialize(result.data[0])

    def get_by_name(self, name: UserName) -> Optional[User]:
        result = (
            self.client.table(self.table).select("*").eq("name", name.value).execute()
        )

        if not result.data:
            return None

        return User.deserialize(result.data[0])

    def get(self, name: UserName) -> list[User]:
        query = self.client.table(self.table).select("*")

        if name is not None:
            query = query.eq("name", name.value)

        result = query.execute()
        return [User.deserialize(data) for data in result.data]

    def update_last_login(self, user_id: UserID, last_login: datetime) -> None:
        self.client.table(self.table).update({"last_login": last_login.isoformat()}).eq(
            "id", str(user_id.value)
        ).execute()

    def update_has_answered(
        self, user_id: UserID, has_answered: UserHasAnswered
    ) -> None:
        self.client.table(self.table).update({"has_answered": has_answered.value}).eq(
            "id", str(user_id.value)
        ).execute()
