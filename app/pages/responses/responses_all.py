import flet as ft

from app.pages.responses.responses_all_week import ResponsesAllWeek
from constants import SECONDARY_COLOR
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

        self.matches = self._get_matches()

        default_match_value = None
        if self.selected_match is not None and len(self.matches) > self.selected_match:
            default_match_value = str(self.matches[self.selected_match].id.value)

        self.match_dropdown = ft.Dropdown(
            options=[
                ft.dropdown.Option(
                    key=match.id.value,
                    content=ft.Container(content=ft.Text(f"{match.local_team.value} vs {match.visitor_team.value}", overflow=ft.TextOverflow.ELLIPSIS), width=300),
                )
                for match in self.matches
            ],
            width=320,
            label="Selecciona el partido",
            on_change=self._match_changer,
            value=default_match_value,
            bgcolor=SECONDARY_COLOR,
        )

        dropdowns = ft.Container(
            content=ft.Column(controls=[self.week_dropdown, self.match_dropdown]),
            padding=ft.Padding(top=50, left=5, right=5, bottom=10),
        )

        self.controls = [dropdowns, ft.Divider(thickness=2.5)]

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

    def _get_matches(self) -> list[Match]:
        week_matches_obj = self.data.matches_by_week.matches.get(
            self.week_dropdown.value
        )
        week_matches = week_matches_obj.matches if week_matches_obj is not None else []
        return [
            match for date_matches in week_matches for match in date_matches.matches
        ]

    def _week_changer(self, event: ft.ControlEvent):
        if self.week_dropdown.value is not None:
            self.selected_week = self.weeks.index(self.week_dropdown.value)

        self.match_dropdown.value = None

        self.update()

    def _match_changer(self, event: ft.ControlEvent):
        if self.match_dropdown.value is not None:
            self.selected_match = [str(match.id.value) for match in self.matches].index(
                self.match_dropdown.value
            )

        self.update()
