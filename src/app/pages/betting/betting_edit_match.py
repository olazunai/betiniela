import flet as ft

from app.pages.betting.betting_form_match import BettingFormMatch
from core.application.response.response_updater_service import ResponseUpdaterService
from core.domain.entities.match import Match
from core.domain.entities.response import Response


class BettingEditMatch(ft.AlertDialog):
    def __init__(self, match: Match, response: Response):
        super().__init__()

        self.response = response
        self.match = match

    def build(self):
        self._build_function()

    def _build_function(self):
        self.modal = False

        self.form_match = BettingFormMatch(match=self.match, visible=True)

        self.content = ft.Container(
            content=self.form_match,
            height=300,
        )
        self.actions = [
            ft.TextButton("Actualizar", on_click=self._update_response),
        ]

        self.actions_alignment = ft.MainAxisAlignment.CENTER

    def _update_response(self, event: ft.ControlEvent):
        response_updater_service: ResponseUpdaterService = (
            self.page.container.services.response_updater_service()
        )

        response_updater_service(
            response_id=self.response.id.value,
            winner_team=self.form_match.data.winner,
            losser_points=self.form_match.data.losser,
        )

        self.page.close(self)
        self.page.update()
