from dataclasses import dataclass
from typing import Optional

from core.domain.dtos.matches_by_week import MatchesByWeek
from core.domain.entities.ranking import Ranking
from core.domain.entities.user import User


@dataclass
class Data:
    matches_by_week: MatchesByWeek
    rankings: list[Ranking]
    user: Optional[User] = None
