from abc import ABC, abstractmethod
from typing import Optional

from core.domain.entities.match import MatchID
from core.domain.entities.response import Response, ResponseID, ResponseLosserPoints
from core.domain.entities.user import UserID
from core.domain.value_objects.team import Team
from core.domain.value_objects.week import Week


class ResponseRepository(ABC):
    @abstractmethod
    def add(self, response: Response) -> None:
        pass

    @abstractmethod
    def get_by_id(self, response_id: ResponseID) -> Optional[Response]:
        pass

    @abstractmethod
    def get(
        self, week: Week = None, match_id: MatchID = None, user_id: UserID = None
    ) -> list[Response]:
        pass

    @abstractmethod
    def update_data(
        self, response_id: ResponseID, winner: Team, losser_points: ResponseLosserPoints
    ) -> None:
        pass
