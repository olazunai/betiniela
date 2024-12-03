import flet as ft

from app.widgets.dropdown import Dropdown
from core.domain.dtos.betting_form_match_data import BettingFormMatchData
from core.domain.entities.match import MatchID


class BettingFormMatch(ft.Container):
    def __init__(
        self, match_id: MatchID, local_team: str, visitor_team: str, visible: bool
    ):
        super().__init__()

        self.visible = visible

        self.data = BettingFormMatchData(match_id=match_id)

        self.winner = ft.RadioGroup(
            content=ft.Row(
                controls=[
                    ft.Text("Ganador:"),
                    ft.Column(
                        controls=[
                            ft.Radio(value=local_team, label=local_team, width=180),
                            ft.Radio(value=visitor_team, label=visitor_team, width=180),
                        ],
                    ),
                ],
                wrap=True,
                expand=True,
            ),
            on_change=self._winner_changer,
        )

        self.losser = Dropdown(
            options=[
                "0-6 tantos",
                "7-11 tantos",
                "12-15 tantos",
                "16-18 tantos",
                "19-21 tantos",
            ],
            label="Perdedor",
            label_size=12,
            on_change=self._losser_changer,
            text_size=12,
            width=150,
        )

        divider = ft.Divider(thickness=0.5)

        self.content = ft.Column(
            controls=[divider, self.winner, self.losser],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _winner_changer(self, event: ft.ControlEvent):
        self.data.winner = event.data

    def _losser_changer(self, event: ft.ControlEvent):
        self.data.losser = event.data.replace(" tantos", "")
