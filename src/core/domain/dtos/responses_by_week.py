from dataclasses import dataclass

from core.domain.entities.response import Response


@dataclass
class ResponsesByWeek:
    responses: dict[str, list[Response]]
