import flet as ft

from app.pages.betting.betting_match import BettingMatch
from src.core.application.response.response_list_service import ResponseListService
from src.core.domain.dtos.data import Data
from src.core.domain.dtos.matches_by_week import MatchesByDate
from src.core.domain.entities.response import Response
from src.core.domain.value_objects.week import Week


class BettingWeek(ft.Container):
    def __init__(self, week: Week, data: Data, visible: bool):
        super().__init__()
        self.data: Data = data

        self.visible = visible
        self.week = week

    def build(self):
        self._build_function()

    def before_update(self):
        response_list_service: ResponseListService = (
            self.page.container.services.response_list_service
        )

        responses = response_list_service(week=self.week)
        self.data.responses_by_week.responses.update(responses.responses)

        self.build()

    def _build_function(self):
        self.week_responses: list[Response] = self.data.responses_by_week.responses.get(
            self.week.name(), []
        )
        self.week_matches: MatchesByDate = self.data.matches_by_week.matches.get(
            self.week.name(), MatchesByDate(matches=[])
        )

        self.responses = []
        for response in self.week_responses:
            match_id = response.match_id.value
            for date_matches in self.week_matches.matches:
                for match in date_matches.matches:
                    if match.id.value != match_id:
                        continue

                    self.responses.append(BettingMatch(match=match, response=response))

        self.no_response = ft.Container(
            content=ft.Text(
                "No hay respuestas para esta semana.",
                visible=not bool(self.responses),
                text_align=ft.TextAlign.CENTER,
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.only(top=20),
        )
        self.content = ft.Column(controls=self.responses + [self.no_response])
