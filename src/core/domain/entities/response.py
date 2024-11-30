from datetime import datetime
from enum import StrEnum
from typing import Optional
from uuid import UUID
from attr import dataclass

from core.domain.entities.match import MatchID
from core.domain.entities.user import UserID
from core.domain.value_objects.team import Team
from core.domain.value_objects.week import Week


@dataclass
class ResponseID:
    value: UUID


class ResponseLosserPoints(StrEnum):
    0_6 = "0-6"
    7_11 = "7-11"
    12_15 = "12-15"
    16_18 = "16-18"
    19_21 = "19-21"


@dataclass
class Response:
    id: ResponseID
    week: Week
    match_id: MatchID
    user_id: UserID
    winner: Team
    losser_points: ResponseLosserPoints
    response_time: datetime
    updated_time: Optional[datetime] = None
