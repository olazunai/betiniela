import flet as ft

from app.pages.betting.betting_match import BettingMatch
from app.widgets.snack_bar import SnackBar
from app.utils import is_week_started
from src.core.domain.entities.user import UserRole
from src.core.application.response.response_creator_service import (
    ResponseCreatorService,
)
from src.core.domain.dtos.data import Data


class BettingWeek(ft.Container):
    def __init__(self, week_name: str, data: Data, visible: bool):
        super().__init__()

        self.week_name = week_name
        self.data: Data = data
        self.visible = visible
        self.expand = True

    def build(self):
        self._build_function()

    def _build_function(self):
        self.padding = ft.Padding(
            left=5,
            right=5,
            top=5,
            bottom=5,
        )
        self.expand = True
        self.answered = False

        self.betting_matches = []

        week_matches_obj = self.data.matches_by_week.matches.get(self.week_name)
        week_matches = week_matches_obj.matches if week_matches_obj is not None else []
        for matches in week_matches:
            for match in matches.matches:
                self.betting_matches.append(BettingMatch(match=match))

        self.sent_success = SnackBar(
            text="Quiniela enviada correctamente", success=True, open=False
        )
        self.sent_error = SnackBar(
            text="Ha ocurrido un error enviando la quiniela", success=False, open=False
        )
        self.sent_invalid = SnackBar(
            text="Tienes que rellenar todos los apartados", success=False, open=False
        )

        self.submit_button = ft.Container(
            content=ft.ElevatedButton(
                text="Enviar respuesta",
                on_click=self._send_response,
            ),
            alignment=ft.alignment.center,
            margin=ft.margin.only(top=30, bottom=30),
        )

        self.content = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=self.betting_matches,
                        expand=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ),
                self.submit_button,
                self.sent_error,
                self.sent_invalid,
                self.sent_success,
            ],
            expand=True,
            scroll=ft.ScrollMode.ALWAYS,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self.user_dropdown = ft.Dropdown(
            options=[
                ft.dropdown.Option(key=str(user.id.value), text=user.name.value)
                for user in self.data.users
            ],
            label="Selecciona el usuario",
        )

        if self.data.user.role == UserRole.SUPERUSER:
            self.content.controls.insert(0, self.user_dropdown)

    def _send_response(self, event: ft.ControlEvent):
        response_creator_service: ResponseCreatorService = (
            self.page.container.services.response_creator_service
        )

        if is_week_started(
            data=self.data, week_name=self.week_name
        ):
            self.page.overlay.append(
                SnackBar(
                    text="La jornada ya ha empezado y no se pueden enviar respuestas",
                    success=False,
                    open=True,
                ),
            )
            self.page.update()
            return

        for betting_match in self.betting_matches:
            if not all(
                [
                    betting_match.data.match_id.value,
                    betting_match.data.winner,
                    betting_match.data.losser,
                ]
            ):
                self.sent_invalid.open = True
                self.update()
                return

        try:
            user = self.data.user
            if self.user_dropdown.value is not None:
                user = [
                    usr
                    for usr in self.data.users
                    if str(usr.id.value) == self.user_dropdown.value
                ][0]

            for betting_match in self.betting_matches:
                response_creator_service(
                    week_name=self.week_name,
                    match_id=betting_match.data.match_id.value,
                    user_id=user.id.value,
                    user_name=user.name.value,
                    winner_team=betting_match.data.winner,
                    losser_points=betting_match.data.losser,
                )

            self.sent_success.open = True
        except Exception as e:
            self.sent_error.open = True

        self.update()

        self.page.update()
