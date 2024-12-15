from typing import Optional
import flet as ft

from app.widgets.dropdown import Dropdown
from src.core.domain.dtos.betting_form_match_data import BettingFormMatchData
from src.core.domain.entities.match import Match
from src.core.domain.entities.response import Response


class BettingMatch(ft.Container):
    def __init__(
        self,
        match: Match,
        response: Optional[Response] = None,
        show_divider: Optional[bool] = True,
    ):
        super().__init__()

        self.expand = True

        self.winner = ft.RadioGroup(
            content=ft.Column(
                controls=[
                    ft.Text("Ganador:"),
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
            width=160,
            selected_index=(
                options.index(response.losser_points.value)
                if response is not None
                else None
            ),
        )

        column_content = [self.winner, self.losser]

        if show_divider:
            column_content.insert(0, ft.Divider(thickness=2.5))

        self.content = ft.Column(
            controls=column_content,
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
