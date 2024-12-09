from typing import Optional
import flet as ft

from app.widgets.dropdown import Dropdown
from src.core.domain.dtos.betting_form_match_data import BettingFormMatchData
from src.core.domain.entities.match import Match
from src.core.domain.entities.response import Response


class BettingFormMatch(ft.Container):
    def __init__(
        self, match: Match, visible: bool, response: Optional[Response] = None
    ):
        super().__init__()

        self.visible = visible

        self.winner = ft.RadioGroup(
            content=ft.Row(
                controls=[
                    ft.Text("Ganador:"),
                    ft.Column(
                        controls=[
                            ft.Radio(
                                value=match.local_team.value,
                                label=match.local_team.value,
                                width=180,
                            ),
                            ft.Radio(
                                value=match.visitor_team.value,
                                label=match.visitor_team.value,
                                width=180,
                            ),
                        ],
                    ),
                ],
                wrap=True,
                expand=True,
            ),
            on_change=self._winner_changer,
            value=response.winner.value if response is not None else None,
        )

        options = [
            "0-6",
            "7-11",
            "12-15",
            "16-18",
            "19-21",
        ]
        self.losser = Dropdown(
            options=options,
            label="Tantos del perdedor",
            label_size=12,
            on_change=self._losser_changer,
            text_size=12,
            width=150,
            selected_index=(
                options.index(response.losser_points.value)
                if response is not None
                else None
            ),
        )

        divider = ft.Divider(thickness=0.5)

        self.content = ft.Column(
            controls=[divider, self.winner, self.losser, divider],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self.data = BettingFormMatchData(
            match_id=match.id,
            winner=self.winner.value,
            losser=self.losser.value,
        )

    def _winner_changer(self, event: ft.ControlEvent):
        self.data.winner = event.data

    def _losser_changer(self, event: ft.ControlEvent):
        self.data.losser = event.data
