import flet as ft

from app.pages.responses.responses_all_week import ResponsesAllWeek
from src.core.domain.entities.match import Match
from src.core.domain.dtos.data import Data
from src.core.domain.value_objects.week import Week


class ResponsesAll(ft.Container):
    def __init__(self, data: Data):
        super().__init__()

        self.data: Data = data
        self.weeks = sorted(data.matches_by_week.matches.keys())
        self.selected_match = None

    def build(self):
        self.selected_week = sorted(self.data.matches_by_week.matches.keys()).index(
            self.data.config.current_week.name()
        )
        self._build_function()

    def before_update(self):
        self.data = self.page.data
        self._build_function()

    def _build_function(self):
        self.week_dropdown = ft.Dropdown(
            options=[ft.dropdown.Option(option) for option in self.weeks],
            width=200,
            label="Selecciona la jornada",
            on_change=self._week_match_changer,
            value=(
                self.weeks[self.selected_week]
                if self.selected_week is not None
                else None
            ),
        )

        self.matches: list[Match] = [
            match
            for date_matches in self.data.matches_by_week.matches[
                self.week_dropdown.value
            ].matches
            for match in date_matches.matches
        ]
        self.match_dropdown = ft.Dropdown(
            options=[
                ft.dropdown.Option(
                    key=match.id.value,
                    text=f"{match.local_team.value} vs {match.visitor_team.value}",
                )
                for match in self.matches
            ],
            width=400,
            label="Selecciona el partido",
            on_change=self._week_match_changer,
            value=(
                str(self.matches[self.selected_match].id.value)
                if self.selected_match is not None
                else None
            ),
        )

        dropdowns = ft.Container(
            content=ft.Column(controls=[self.week_dropdown, self.match_dropdown]),
            padding=ft.Padding(top=50, left=5, right=5, bottom=10),
        )

        self.controls = [dropdowns]

        if (
            self.week_dropdown.value is not None
            and self.match_dropdown.value is not None
        ):
            self.controls.append(
                ResponsesAllWeek(
                    week=Week.deserialize(self.week_dropdown.value),
                    match_id=self.match_dropdown.value,
                    data=self.data,
                )
            )

        self.content = ft.Column(
            controls=self.controls,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _week_match_changer(self, event: ft.ControlEvent):
        if self.selected_week is not None:
            self.selected_week = self.weeks.index(self.week_dropdown.value)

        if self.match_dropdown.value is not None:
            self.selected_match = [str(match.id.value) for match in self.matches].index(
                self.match_dropdown.value
            )

        self.update()
