import flet as ft

from app.pages.betting.betting_match import BettingMatch
from core.domain.dtos.data import Data
from core.domain.dtos.matches_by_week import MatchesByDate
from core.domain.entities.response import Response
from core.domain.value_objects.week import Week


class BettingWeek(ft.Container):
    def __init__(self, week: Week, data: Data, visible: bool):
        super().__init__()

        self.visible = visible
        self.week = week

        self.week_responses: list[Response] = data.responses_by_week.responses.get(week.name(), [])
        self.week_matches: MatchesByDate = data.matches_by_week.matches.get(week.name(), MatchesByDate(matches=[]))

        self.responses = []
        for response in self.week_responses:
            match_id = response.match_id.value
            for date_matches in self.week_matches.matches:
                for match in date_matches.matches:
                    if match.id.value != match_id:
                        continue

                    self.responses.append(
                        BettingMatch(
                            local_team=match.local_team.value,
                            visitor_team=match.visitor_team.value,
                            winner=response.winner.value,
                            losser=response.losser_points.value,
                        )
                    )

        self.no_response = ft.Container(
            content=ft.Text(
                "No hay respuestas para esta semana.",
                visible=not bool(self.responses),
                text_align=ft.TextAlign.CENTER,
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.only(top=20),
        )
        self.content = ft.Column(
            controls=self.responses + [self.no_response]
        )
