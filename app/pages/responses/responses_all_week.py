from datetime import datetime
from uuid import UUID
import flet as ft

from src.core.domain.entities.match import Match, MatchID
from src.core.application.response.response_list_service import ResponseListService
from src.core.domain.dtos.data import Data
from src.core.domain.entities.response import Response
from src.core.domain.value_objects.week import Week


class ResponsesAllWeek(ft.Container):
    def __init__(self, week: Week, match_id: str, data: Data):
        super().__init__()

        self.data: Data = data
        self.week = week
        self.match_id: MatchID = MatchID(UUID(match_id))
        self.expand = True

        self.alignment = ft.alignment.center

    def build(self):
        self._build_function()

    def before_update(self):
        response_list_service: ResponseListService = (
            self.page.container.services.response_list_service
        )

        responses = response_list_service(week=self.week)
        self.data.responses_by_week.responses.update(responses.responses)

        self._build_function()

    def _build_function(self):
        week_responses: list[Response] = self.data.responses_by_week.responses.get(
            self.week.name(), []
        )
        match_responses: list[Response] = [response for response in week_responses if response.match_id == self.match_id]

        self.no_response = ft.Container(
            content=ft.Text(
                "Respuestas no disponibles para esta semana.",
                text_align=ft.TextAlign.CENTER,
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.only(top=20),
        )

        self.data_table = ft.Container(
            content=ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text(" ")),
                    ft.DataColumn(ft.Text("Ganador")),
                    ft.DataColumn(ft.Text("Tantos perdedor")),
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(response.user_name.value)),
                            ft.DataCell(ft.Text(response.winner.value)),
                            ft.DataCell(ft.Text(response.losser_points.value)),
                        ],
                    ) for response in match_responses
                ],
                data_row_max_height=float("inf")
            ),
        )

        first_match: Match = sorted(sorted(self.data.matches_by_week.matches[self.week.name()].matches, key=lambda x: x.day)[0].matches, key=lambda x: x.match_time)[0]
        if datetime.now() < datetime.combine(first_match.match_day, first_match.match_time):
            self.content = self.no_response
        elif match_responses:
            self.content = self.data_table
        else:
            self.content = self.no_response
