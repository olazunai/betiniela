from dataclasses import dataclass
from datetime import date

from core.domain.entities.match import Match
from core.domain.value_objects.week import Week


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
