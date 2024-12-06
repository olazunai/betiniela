from dataclasses import dataclass
from typing import Optional

from core.domain.dtos.matches_by_week import MatchesByWeek
from core.domain.dtos.responses_by_week import ResponsesByWeek
from core.domain.entities.config import Config
from core.domain.entities.ranking import Ranking
from core.domain.entities.user import User


@dataclass
class Data:
    matches_by_week: MatchesByWeek
    responses_by_week: ResponsesByWeek
    rankings: list[Ranking]
    config: Config
    user: Optional[User] = None
