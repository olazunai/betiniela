from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from src.core.domain.entities.user import UserID
from src.core.domain.dtos.responses_by_week import ResponsesByWeek
from src.core.domain.entities.response import Response
from src.core.domain.repositories.response_repository import ResponseRepository
from src.core.domain.value_objects.week import Week


@dataclass
class ResponseListService:
    response_repository: ResponseRepository

    def __call__(
        self, week: Optional[Week] = None, user_id: Optional[UUID] = None
    ) -> ResponsesByWeek:
        responses = self.response_repository.get(
            week=week, user_id=UserID(user_id) if user_id is not None else None
        )

        responses_by_week = self._divide_responses_by_week(responses)
        return ResponsesByWeek(responses=responses_by_week)

    @staticmethod
    def _divide_responses_by_week(
        responses: list[Response],
    ) -> dict[str, list[Response]]:
        responses_by_week = {}
        for response in responses:
            responses_by_week[response.week.name()] = responses_by_week.get(
                response.week.name(), []
            ) + [response]

        return responses_by_week
