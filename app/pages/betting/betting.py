from calendar import week
from datetime import datetime
import flet as ft

from app.pages.betting.betting_week import BettingWeek
from app.utils import is_week_started
from constants import SECONDARY_COLOR
from src.core.domain.value_objects.week import Week
from src.core.application.response.response_list_service import ResponseListService
from src.core.domain.dtos.responses_by_week import ResponsesByWeek
from src.core.domain.dtos.data import Data


class Betting(ft.Container):
    def __init__(self, data: Data):
        super().__init__()

        self.data: Data = data
        self.week_name = self.data.config.current_week.name()

        self.responses_by_week: ResponsesByWeek = self.data.responses_by_week

    def build(self):
        try:
            self.selected_week = sorted(self.data.matches_by_week.matches.keys()).index(
                self.data.config.current_week.name()
            )
        except ValueError:
            self.selected_week = None

        self._build_function()

    def before_update(self):
        response_list_service: ResponseListService = (
            self.page.container.services.response_list_service
        )

        week_name = self.week_dropdown.value or self.week_name

        responses = response_list_service(week=Week.deserialize(week_name))
        self.data.responses_by_week.responses.update(responses.responses)

        self._build_function()

    def _build_function(self):
        self.weeks = sorted(self.data.matches_by_week.matches.keys())

        self.expand = True

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

        self.has_answered = self._has_answered()

        self.no_available = True
        if self.week_dropdown.value is not None:
            self.no_available = is_week_started(
                data=self.data, week_name=self.week_dropdown.value
            )

        self.answered_form = ft.Container(
            content=ft.Text(
                "Ya has rellenado la quiniela de esta semana. Puedes editarla desde las respuestas.",
                text_align=ft.TextAlign.CENTER,
                expand=True,
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.only(bottom=30, left=50, right=50, top=100),
        )
        self.no_form = ft.Container(
            content=ft.Text(
                "La jornada ya ha empezado y no se pueden cambiar las respuestas.",
                text_align=ft.TextAlign.CENTER,
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.only(bottom=30, left=50, right=50, top=100),
            visible=self.no_available,
        )

        self.form = BettingWeek(
            week_name=self.week_dropdown.value,
            data=self.data,
            visible=True,
        )

        dropdown = ft.Container(
            content=self.week_dropdown, padding=ft.padding.only(top=20, left=5)
        )

        self.content = ft.Column(
            controls=[dropdown],
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        if self.no_available:
            self.content.controls.append(self.no_form)

        elif self.has_answered:
            self.content.controls.append(self.answered_form)

        else:
            self.content.controls.append(self.form)

    def _week_changer(self, event: ft.ControlEvent):
        if self.selected_week is not None:
            self.selected_week = sorted(self.data.matches_by_week.matches.keys()).index(
                self.week_dropdown.value
            )

        self.update()

    def _has_answered(self):
        if self.week_dropdown.value is None:
            return True

        week_matches_obj = self.data.matches_by_week.matches.get(
            self.week_dropdown.value
        )
        week_matches = week_matches_obj.matches if week_matches_obj is not None else []
        matches = [match for week_match in week_matches for match in week_match.matches]

        week_responses = self.data.responses_by_week.responses.get(
            self.week_dropdown.value, []
        )
        responses = [
            response
            for response in week_responses
            if response.user_id.value == self.data.user.id.value
        ]

        return len(responses) == len(matches)
