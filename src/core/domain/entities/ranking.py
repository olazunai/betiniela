from uuid import UUID
from attr import dataclass

from core.domain.entities.user import UserID
from core.domain.value_objects.team import Team


@dataclass
class RankingID:
    value: UUID


@dataclass
class RankingPosition:
    value: int


@dataclass
class RankingPoints:
    value: int


@dataclass
class Ranking:
    id: RankingID
    week: Team
    user_id: UserID
    position: RankingPosition
    points: RankingPoints
