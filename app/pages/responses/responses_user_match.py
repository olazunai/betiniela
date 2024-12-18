import flet as ft

from app.pages.responses.edit_response_modal import EditResponseModal
from app.utils import is_week_started
from src.core.domain.dtos.data import Data
from src.core.domain.entities.match import Match
from src.core.domain.entities.response import Response


class ResponsesUserMatch(ft.Container):
    def __init__(self, data: Data, match: Match, response: Response):
        super().__init__()

        self.response = response
        self.match = match
        self.data: Data = data

    def build(self):
        self._build_function()

    def _build_function(self):
        self.header = ft.Row(
            controls=[
                ft.Container(content=ft.Divider(thickness=0.5), expand=True),
                ft.Text(
                    value=f"{self.match.local_team.value} vs {self.match.visitor_team.value}",
                    opacity=0.8,
                ),
                ft.Container(content=ft.Divider(thickness=0.5), expand=True),
            ],
            expand=True,
        )

        self.result = ft.Column(
            controls=[
                ft.Text(
                    value=f"Ganador:    {self.response.winner.value}", no_wrap=True
                ),
                ft.Text(
                    value=f"Perdedor:    {self.response.losser_points.value} tantos",
                    no_wrap=True,
                ),
            ],
            spacing=30,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        self.edit_button = ft.Container(
            content=ft.IconButton(
                icon=ft.Icons.EDIT,
                on_click=self._edit_response_modal,
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.only(right=20),
        )

        self.response_container = ft.Container(
            content=ft.Row(
                controls=[self.result],
                spacing=30,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            alignment=ft.alignment.center,
            margin=ft.Margin(
                left=15,
                right=5,
                top=20,
                bottom=20,
            ),
            width=500,
        )

        if not is_week_started(data=self.data, week_name=self.match.week.name()):
            self.response_container.content.controls.append(self.edit_button)

        self.betting_match = ft.Column(
            controls=[self.header, self.response_container],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self.edit_response = EditResponseModal(response=self.response, match=self.match, data=self.data)

        self.content = self.betting_match

    def _edit_response_modal(self, event: ft.ControlEvent):
        self.page.open(self.edit_response)
