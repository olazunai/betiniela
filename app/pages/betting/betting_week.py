import flet as ft

from app.pages.betting.betting_match import BettingMatch
from app.widgets.snack_bar import SnackBar
from src.core.application.response.response_creator_service import ResponseCreatorService
from src.core.application.user.user_has_answered_updater_service import (
    UserHasNasweredUpdaterService,
)
from src.core.domain.dtos.data import Data


class BettingWeek(ft.Container):
    def __init__(self, week_name: str, data: Data, visible: bool):
        super().__init__()

        self.week_name = week_name
        self.data: Data = data
        self.visible = visible

    def build(self):
        self._build_function()

    def _build_function(self):
        self.padding = ft.Padding(
            left=50,
            right=50,
            top=5,
            bottom=5,
        )
        self.expand = True
        self.answered = False

        self.betting_matches = []
        for matches in self.data.matches_by_week.matches[self.week_name].matches:
            for match in matches.matches:
                self.betting_matches.append(BettingMatch(match=match))

        self.sent_success = SnackBar(text="Quiniela enviada correctamente", success=True, open=False)
        self.sent_error = SnackBar(text="Ha ocurrido un error enviando la quiniela", success=False, open=False)
        self.sent_invalid = SnackBar(text="Tienes que rellenar todos los apartados", success=False, open=False)

        self.submit_button = ft.Container(
            content=ft.ElevatedButton(
                text="Enviar respuesta", on_click=self._send_response,
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

    def _send_response(self, event: ft.ControlEvent):
        response_creator_service: ResponseCreatorService = (
            self.page.container.services.response_creator_service
        )
        user_has_answered_updater_service: UserHasNasweredUpdaterService = (
            self.page.container.services.user_has_answered_updater_service
        )

        for betting_match in self.betting_matches:
            if not all([betting_match.data.match_id.value, betting_match.data.winner, betting_match.data.losser]):
                self.sent_invalid.open = True
                self.update()
                return

        try:
            for betting_match in self.betting_matches:
                response_creator_service(
                    week_name=self.week_name,
                    match_id=betting_match.data.match_id.value,
                    user_id=self.data.user.id.value,
                    winner_team=betting_match.data.winner,
                    losser_points=betting_match.data.losser,
                )

            user_has_answered_updater_service(
                user_id=self.data.user.id.value,
                has_answered=True,
            )

            self.sent_success.open = True
        except Exception as e:
            self.sent_error.open = True

        self.update()

        self.page.update()
