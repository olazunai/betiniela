from abc import ABC, abstractmethod
from typing import Optional

from core.domain.entities.match import MatchID
from core.domain.entities.response import Response, ResponseID
from core.domain.entities.user import UserID
from core.domain.value_objects.week import Week


class ResponseRepository(ABC):
    @abstractmethod
    async def add(self, response: Response) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, response_id: ResponseID) -> Optional[Response]:
        pass

    @abstractmethod
    async def get(
        self, week: Week = None, match_id: MatchID = None, user_id: UserID = None
    ) -> list[Response]:
        pass

    @abstractmethod
    async def update(self, response: Response) -> None:
        pass
