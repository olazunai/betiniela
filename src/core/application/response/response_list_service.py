from dataclasses import dataclass

from core.domain.dtos.responses_by_week import ResponsesByWeek
from core.domain.entities.response import Response
from core.domain.repositories.response_repository import ResponseRepository


@dataclass
class ResponseListService:
    response_repository: ResponseRepository

    async def __call__(self) -> ResponsesByWeek:
        responses = await self.response_repository.get()

        responses_by_week = await self._divide_responses_by_week(responses)
        return ResponsesByWeek(responses=responses_by_week)

    @staticmethod
    async def _divide_responses_by_week(responses: list[Response]) -> dict[str, list[Response]]:
        responses_by_week = {}
        for response in responses:
            responses_by_week[response.week.name()] = responses_by_week.get(
                response.week.name(), []
            ) + [response]

        return responses_by_week
