import flet as ft

from app.pages.betting.betting_match import BettingMatch
from app.widgets.snack_bar import SnackBar
from app.utils import is_week_started
from src.core.domain.dtos.data import Data
from src.core.application.response.response_updater_service import (
    ResponseUpdaterService,
)
from src.core.domain.entities.match import Match
from src.core.domain.entities.response import Response


class EditResponseModal(ft.AlertDialog):
    def __init__(self, match: Match, response: Response, data: Data):
        super().__init__()

        self.response = response
        self.match = match
        self.data = data

    def build(self):
        self._build_function()

    def _build_function(self):
        self.modal = False

        self.form_match = BettingMatch(
            match=self.match, response=self.response, show_divider=False
        )

        self.content = ft.Container(
            content=self.form_match,
            height=250,
        )
        self.actions = [
            ft.TextButton("Actualizar", on_click=self._update_response),
        ]

        self.actions_alignment = ft.MainAxisAlignment.CENTER

    def _update_response(self, event: ft.ControlEvent):
        response_updater_service: ResponseUpdaterService = (
            self.page.container.services.response_updater_service
        )
        
        if is_week_started(
            data=self.data, week_name=self.match.week.name()
        ):
            self.page.close(self)
            self.page.overlay.append(
                SnackBar(
                    text="La jornada ya ha empezado y no se pueden editar respuestas.",
                    success=False,
                    open=True,
                ),
            )
            self.page.update()
            return

        try:
            response_updater_service(
                response_id=self.response.id.value,
                winner_team=self.form_match.data.winner,
                losser_points=self.form_match.data.losser,
            )
            success = True
            text = "Respuesta actualizada correctamente"
        except Exception as e:
            success = False
            text = f"Ha ocurrido un error actualizando la respuesta: {e}"

        self.page.close(self)

        self.page.overlay.append(SnackBar(text=text, success=success, open=True))

        self.page.update()
