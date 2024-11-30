from dataclasses import dataclass
from math import exp
from typing import Optional
import flet as ft

from widgets.dropdown import Dropdown


@dataclass
class BettingFormMatchData:
    winner: Optional[str] = None
    losser: Optional[str] = None


class BettingFormMatch(ft.Container):
    def __init__(self, local_team: str, visitor_team: str):
        super().__init__()

        self.data = BettingFormMatchData()

        self.expand = True
        self.alignment = ft.alignment.top_center

        self.winner = ft.RadioGroup(
            content=ft.Row(
                controls=[
                    ft.Text("Ganador:"),
                    ft.Column(
                        controls=[
                            ft.Radio(value=local_team, label=local_team, width=180),
                            ft.Radio(value=visitor_team, label=visitor_team, width=180),
                        ],
                    )
                ],
                wrap=True,
                expand=True,
            ),
            on_change=self._winner_changer
        )
    
        self.losser = Dropdown(
            options=["0-6 tantos", "7-11 tantos", "12-15 tantos", "16-18 tantos", "19-21 tantos"],
            label="Perdedor",
            label_size=12,
            on_change=self._losser_changer,
            text_size=12,
            width=150,
        )


        self.content = ft.Column(
            controls=[
                self.winner,
                self.losser
            ],
            expand=True,
        )

    def _winner_changer(self, event: ft.ControlEvent):
        self.data.winner = event.data

    def _losser_changer(self, event: ft.ControlEvent):
        self.data.losser = event.data
