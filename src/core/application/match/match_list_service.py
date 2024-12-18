from dataclasses import dataclass

from src.core.domain.dtos.matches_by_week import (
    DateMatches,
    MatchesByDate,
    MatchesByWeek,
)
from src.core.domain.entities.match import Match
from src.core.domain.repositories.match_repository import MatchRepository


@dataclass
class MatchListService:
    match_repository: MatchRepository

    def __call__(self) -> MatchesByWeek:
        matches = self.match_repository.get()

        matches_by_week = self._divide_matches_by_week(matches)
        return MatchesByWeek(
            matches={
                week: MatchesByDate(matches=self._divide_matches_by_date(matches))
                for week, matches in matches_by_week.items()
            }
        )

    @staticmethod
    def _divide_matches_by_week(matches: list[Match]) -> dict[str, list[Match]]:
        matches_by_week = {}
        for match in matches:
            matches_by_week[match.week.name()] = matches_by_week.get(
                match.week.name(), []
            ) + [match]

        return matches_by_week

    @staticmethod
    def _divide_matches_by_date(matches: list[Match]) -> DateMatches:
        matches_by_date = {}
        for match in matches:
            matches_by_date[match.match_day] = matches_by_date.get(
                match.match_day, []
            ) + [match]

        return sorted(
            [
                DateMatches(
                    day=day,
                    matches=matches,
                )
                for day, matches in matches_by_date.items()
            ],
            key=lambda x: x.day,
        )
