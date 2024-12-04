from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from core.domain.entities.response import (
    Response,
    ResponseID,
    ResponseLosserPoints,
)
from core.domain.exceptions import ResponseDoesNotExistsException
from core.domain.repositories.response_repository import ResponseRepository
from core.domain.value_objects.team import Team


@dataclass
class ResponseUpdaterService:
    response_repository: ResponseRepository

    def __call__(
        self,
        response_id: UUID,
        winner_team: str,
        losser_points: str,
    ) -> Optional[Response]:
        losser_points = "0-6"
        response = self.response_repository.get_by_id(
            response_id=ResponseID(response_id),
        )
        if response is None:
            raise ResponseDoesNotExistsException(
                f"Trying to update a non existing response with {response_id} ID."
            )

        self.response_repository.update_data(
            response_id=ResponseID(response_id),
            winner=Team(winner_team),
            losser_points=ResponseLosserPoints(losser_points),
        )
        response.losser_points = ResponseLosserPoints(losser_points)
        return response
