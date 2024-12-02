from dataclasses import dataclass

from core.domain.dtos.matches_by_week import MatchesByWeek
from core.domain.entities.ranking import Ranking


@dataclass
class Data:
    matches_by_week: MatchesByWeek
    rankings: list[Ranking]
