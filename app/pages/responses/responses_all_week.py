from uuid import UUID
import flet as ft

from app.utils import is_week_started
from constants import SECONDARY_COLOR
from src.core.domain.entities.match import MatchID
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
        match_responses: list[Response] = [
            response
            for response in week_responses
            if response.match_id == self.match_id
        ]

        self.no_response = ft.Container(
            content=ft.Text(
                "Respuestas no disponibles para esta semana.",
                text_align=ft.TextAlign.CENTER,
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.only(top=20),
        )

        divided_responses = self._divide_responses(match_responses)

        self.expansions = []

        for winner, responses in divided_responses.items():
            self.expansions.append(
                ft.ExpansionTile(
                    title=ft.Text(winner),
                    maintain_state=True,
                    initially_expanded=True,
                    bgcolor=SECONDARY_COLOR,
                    controls=[self._create_data_table(responses)],
                    expanded_alignment=ft.alignment.center,
                    expanded_cross_axis_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )

        if not is_week_started(data=self.data, week_name=self.week.name()):
            self.content = self.no_response

        elif match_responses:
            self.content = ft.Column(controls=self.expansions, scroll=ft.ScrollMode.ALWAYS)

        else:
            self.content = self.no_response

    def _create_data_table(self, responses: list[Response]) -> ft.Container:
        return ft.Container(
            content=ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text(" ")),
                    ft.DataColumn(ft.Text("Tanteo perdedor")),
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(
                                ft.Container(
                                    content=ft.Text(
                                        response.user_name.value,
                                        overflow=ft.TextOverflow.ELLIPSIS,
                                    ),
                                    width=120,
                                )
                            ),
                            ft.DataCell(ft.Text(response.losser_points.value)),
                        ],
                    )
                    for response in responses
                ],
                data_row_max_height=float("inf"),
            ),
        )

    def _divide_responses(self, responses: list[Response]) -> dict[str, list[Response]]:
        divided = {}
        for response in responses:
            winner = response.winner.value
            divided[winner] = divided.get(winner, []) + [response]

        return divided
