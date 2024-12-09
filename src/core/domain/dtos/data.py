from dataclasses import dataclass
from typing import Optional

from src.core.domain.dtos.matches_by_week import MatchesByWeek
from src.core.domain.dtos.responses_by_week import ResponsesByWeek
from src.core.domain.entities.config import Config
from src.core.domain.entities.ranking import Ranking
from src.core.domain.entities.user import User


@dataclass
class Data:
    matches_by_week: MatchesByWeek
    responses_by_week: ResponsesByWeek
    rankings: list[Ranking]
    config: Config
    user: Optional[User] = None
