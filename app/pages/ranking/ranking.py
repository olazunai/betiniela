import flet as ft

from app.pages.ranking.ranking_week import RankingWeek
from app.widgets.body import Body
from constants import SECONDARY_COLOR
from src.core.domain.value_objects.week import Week
from src.core.domain.dtos.data import Data


class Ranking(Body):
    def __init__(self, data: Data):
        super().__init__()

        self.spacing = 2
        self.data: Data = data
        self.weeks = sorted(data.matches_by_week.matches.keys())

    def build(self):
        try:
            self.selected_week = sorted(self.data.matches_by_week.matches.keys()).index(
                self.data.config.current_week.name()
            )
        except ValueError:
            self.selected_week = None

        self._build_function()

    def before_update(self):
        self.data = self.page.data
        self._build_function()

    def _build_function(self):
        self.week_dropdown = ft.Dropdown(
            options=[ft.dropdown.Option(option) for option in self.weeks],
            width=200,
            label="Selecciona la jornada",
            on_change=self._week_changer,
            value=(
                self.weeks[self.selected_week]
                if self.selected_week is not None
                else None
            ),
            bgcolor=SECONDARY_COLOR,
        )

        self.controls = [
            ft.Container(
                content=self.week_dropdown, padding=ft.padding.only(top=20, left=5)
            )
        ]

        if self.week_dropdown.value is not None:
            self.controls.append(
                RankingWeek(
                    week=Week.deserialize(self.week_dropdown.value),
                    data=self.data,
                )
            )

        self.content = ft.Column(
            controls=self.controls,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _week_changer(self, event: ft.ControlEvent):
        if self.selected_week is not None:
            self.selected_week = self.weeks.index(self.week_dropdown.value)

        self.update()
