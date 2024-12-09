from dataclasses import dataclass
from datetime import date

from src.core.domain.entities.match import Match


@dataclass
class DateMatches:
    day: date
    matches: list[Match]


@dataclass
class MatchesByDate:
    matches: list[DateMatches]


@dataclass
class MatchesByWeek:
    matches: dict[str, MatchesByDate]
