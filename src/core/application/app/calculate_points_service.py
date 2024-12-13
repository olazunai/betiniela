from dataclasses import dataclass
from typing import Optional
from uuid import uuid4

from src.core.domain.entities.config import Config
from src.core.domain.entities.match import Match
from src.core.domain.entities.ranking import (
    Ranking,
    RankingID,
    RankingPoints,
    RankingRightLosser,
    RankingRightWinner,
)
from src.core.domain.entities.response import Response
from src.core.domain.entities.user import User
from src.core.domain.repositories.config_repository import ConfigRepository
from src.core.domain.repositories.match_repository import MatchRepository
from src.core.domain.repositories.ranking_repository import RankingRepository
from src.core.domain.repositories.response_repository import ResponseRepository
from src.core.domain.repositories.user_repository import UserRepository
from src.core.domain.value_objects.week import Week


@dataclass
class CalculatePointService:
    match_repository: MatchRepository
    response_repository: ResponseRepository
    user_repository: UserRepository
    ranking_repository: RankingRepository
    config_repository: ConfigRepository

    def __call__(self, week_name: str) -> None:
        week = Week.deserialize(week_name)
        users: list[User] = self.user_repository.get()
        for user in users:

            points = 0
            right_losser = 0
            right_winner = 0

            responses: list[Response] = self.response_repository.get(
                user_id=user.id, week=week
            )
            for response in responses:

                match: Optional[Match] = self.match_repository.get_by_id(
                    response.match_id
                )
                if match is None or match.result is None:
                    continue

                actual_points, actual_right_winner, actual_right_losser = (
                    self._compute_match_points(match=match, response=response)
                )
                points += actual_points
                right_winner += actual_right_winner
                right_losser += actual_right_losser

            self._update_or_create_ranking(
                user=user,
                week=week,
                points=points,
                right_losser=right_losser,
                right_winner=right_winner,
            )

    def _compute_match_points(self, match: Match, response: Response):
        config: Config = self.config_repository.get()

        match_winner = (
            match.local_team.value
            if match.result.local_team == 22
            else match.visitor_team.value
        )
        match_losser_points = (
            match.result.local_team
            if match.result.local_team != 22
            else match.result.visitor_team
        )

        points = 0
        right_winner = 0
        right_losser = 0

        if response.winner.value == match_winner:
            points += config.right_winner_points
            right_winner += 1

            if response.losser_points.contains(match_losser_points):
                points += config.right_losser_points
                right_losser += 1

        return points, right_winner, right_losser

    def _update_or_create_ranking(
        self, week: Week, user: User, points: int, right_winner: int, right_losser: int
    ) -> None:
        rankings: list[Ranking] = sorted(
            self.ranking_repository.get(user_name=user.name),
            key=lambda x: x.total_points.value,
        )
        if not rankings:
            ranking = Ranking(
                id=RankingID(uuid4()),
                week=week,
                user_name=user.name,
                points=RankingPoints(points),
                total_points=RankingPoints(points),
                right_losser=RankingRightLosser(right_losser),
                right_winner=RankingRightWinner(right_winner),
            )
        elif rankings[-1].week.name() != week.name():
            ranking = Ranking(
                id=RankingID(uuid4()),
                week=week,
                user_name=user.name,
                points=RankingPoints(points),
                total_points=RankingPoints(rankings[-1].total_points.value + points),
                right_losser=RankingRightLosser(right_losser),
                right_winner=RankingRightWinner(right_winner),
            )
        else:
            previous_total_points = (
                rankings[-2].total_points.value if len(rankings) > 1 else 0
            )

            ranking: Ranking = rankings[-1]
            ranking.points.value = points
            ranking.total_points.value = previous_total_points + points
            ranking.right_losser.value = right_losser
            ranking.right_winner.value = right_winner

        self.ranking_repository.add_or_update(ranking)
