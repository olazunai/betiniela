import flet as ft

from core.application.response.response_updater_service import ResponseUpdaterService
from core.domain.entities.match import Match
from core.domain.entities.response import Response


class BettingMatch(ft.Container):
    def __init__(self, match: Match, response: Response):
        super().__init__()

        self.response = response
        self.match = match

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
                ft.Text(value=f"Ganador: {self.response.winner.value}", no_wrap=True),
                ft.Text(
                    value=f"Perdedor: {self.response.losser_points.value} tantos",
                    no_wrap=True,
                ),
            ],
            spacing=30,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        self.edit_button = ft.Container(
            content=ft.IconButton(
                icon=ft.icons.EDIT,
                on_click=self._edit,
            ),
            alignment=ft.alignment.center,
        )

        self.response_container = ft.Container(
            content=ft.Row(
                controls=[self.result, self.edit_button],
                spacing=30,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            alignment=ft.alignment.center,
            margin=ft.Margin(
                left=5,
                right=5,
                top=20,
                bottom=20,
            ),
            width=500,
        )

        self.content = ft.Column(
            controls=[self.header, self.response_container],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _edit(self, event: ft.ControlEvent):
        response_updater_service: ResponseUpdaterService = (
            self.page.container.services.response_updater_service()
        )

        new_response = response_updater_service(
            response_id=self.response.id.value,
            winner_team=self.response.winner.value,
            losser_points=self.response.losser_points.value,
        )

        self.response = new_response

        self.page.update()
