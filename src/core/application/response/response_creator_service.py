from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from core.domain.entities.match import MatchID
from core.domain.entities.response import (
    Response,
    ResponseID,
    ResponseLosserPoints,
)
from core.domain.entities.user import UserID
from core.domain.exceptions import ResponseAlreadyExistsException
from core.domain.repositories.response_repository import ResponseRepository
from core.domain.value_objects.team import Team
from core.domain.value_objects.week import Week


@dataclass
class ResponseCreatorService:
    response_repository: ResponseRepository

    def __call__(
        self,
        week_name: str,
        match_id: UUID,
        user_id: UUID,
        winner_team: str,
        losser_points: str,
    ) -> None:
        existing_response = self.response_repository.get(
            match_id=MatchID(match_id), user_id=UserID(user_id)
        )
        if existing_response:
            raise ResponseAlreadyExistsException(
                f"There is an existing Response of match {match_id}."
            )

        response = Response(
            id=ResponseID(uuid4()),
            week=Week.deserialize(week_name),
            match_id=MatchID(match_id),
            user_id=UserID(user_id),
            winner=Team(winner_team),
            losser_points=ResponseLosserPoints(losser_points),
            response_time=datetime.now(),
        )

        self.response_repository.add(response)
