from dataclasses import dataclass
from typing import Optional
from uuid import uuid4

from core.domain.entities.config import Config
from core.domain.entities.match import Match
from core.domain.entities.ranking import Ranking, RankingID, RankingPoints
from core.domain.entities.response import Response
from core.domain.entities.user import User
from core.domain.repositories.config_repository import ConfigRepository
from core.domain.repositories.match_repository import MatchRepository
from core.domain.repositories.ranking_repository import RankingRepository
from core.domain.repositories.response_repository import ResponseRepository
from core.domain.repositories.user_repository import UserRepository
from core.domain.value_objects.week import Week


@dataclass
class CalculatePointService:
    match_repository: MatchRepository
    response_repository: ResponseRepository
    user_repository: UserRepository
    ranking_repository: RankingRepository
    config_repository: ConfigRepository

    def __call__(self, week_name: str) -> None:
        week = Week.deserialize(week_name)
        users: list[User] = self.user_respository.get()
        for user in users:

            points = 0

            responses: list[Response] = self.response_repository.get(
                user_id=user.id, week=week
            )
            for response in responses:

                match: Optional[Match] = self.match_repository.get_by_id(
                    response.match_id
                )
                if match is None or match.result is None:
                    continue

                points += self._compute_match_points(match=match, response=response)

            self._update_or_create_ranking(
                user=user,
                week=week,
                points=points,
            )

    def _compute_match_points(self, match: Match, response: Response) -> int:
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

        if response.winner.value == match_winner:
            points += config.right_winner_points

            if response.losser_points.contains(match_losser_points):
                points += config.right_losser_points

        return points

    def _update_or_create_ranking(self, week: Week, user: User, points: int) -> None:
        rankings: list[Ranking] = sorted(
            self.ranking_repository.get(user_id=user.id), key=lambda x: x.total_points
        )
        if not rankings:
            ranking = Ranking(
                id=RankingID(uuid4()),
                week=week,
                user_name=user.name,
                points=RankingPoints(points),
                total_points=RankingPoints(points),
            )
        elif rankings[-1].week.name() != week.name():
            ranking = Ranking(
                id=RankingID(uuid4()),
                week=week,
                user_name=user.name,
                points=RankingPoints(points),
                total_points=RankingPoints(rankings[-1].total_points.value + points),
            )
        else:
            previous_total_points = (
                rankings[-2].total_points.value if rankings > 1 else 0
            )

            ranking: Ranking = rankings[-1]
            ranking.points.value = points
            ranking.total_points.value = previous_total_points + points

        self.ranking_repository.add_or_update(ranking)
