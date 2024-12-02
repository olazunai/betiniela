from dataclasses import dataclass

from core.domain.dtos.matches_by_week import MatchesByWeek


@dataclass
class Data:
    matches_by_week: MatchesByWeek
