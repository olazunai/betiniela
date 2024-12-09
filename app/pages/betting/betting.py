import flet as ft

from app.pages.betting.betting_form_week import BettingFormWeek
from app.pages.betting.betting_week import BettingWeek
from app.widgets.body import Body
from app.widgets.dropdown import Dropdown
from src.core.domain.dtos.data import Data
from src.core.domain.value_objects.week import Week


class Betting(Body):
    def __init__(self, data: Data):
        super().__init__()

        self.data: Data = data
        self.weeks = sorted(data.matches_by_week.matches.keys())

    def build(self):
        self.selected_index = sorted(self.data.matches_by_week.matches.keys()).index(
            self.data.config.current_week.name()
        )
        self._build_function(self.selected_index)

    def before_update(self):
        self.data = self.page.data
        self._build_function(self.selected_index)

    def _build_function(self, selected_index: int):
        betting_title = ft.Container(
            ft.Text(
                "Quiniela",
                text_align=ft.TextAlign.LEFT,
                size=20,
                theme_style=ft.TextThemeStyle.TITLE_SMALL,
                weight=ft.FontWeight.BOLD,
            ),
            margin=ft.margin.only(left=20, bottom=20),
        )

        form = BettingFormWeek(
            week_name=self.data.config.current_week.name(), data=self.data
        )

        divider = ft.Divider()

        responses_title = ft.Container(
            ft.Text(
                "Tus respuestas",
                text_align=ft.TextAlign.LEFT,
                size=20,
                theme_style=ft.TextThemeStyle.TITLE_SMALL,
                weight=ft.FontWeight.BOLD,
            ),
            margin=ft.margin.only(left=20, bottom=20),
        )

        self.options = self.weeks
        self.views = [
            BettingWeek(week=Week.deserialize(option), data=self.data, visible=True)
            for option in self.options
        ]

        self.dropdown = Dropdown(
            options=self.options,
            label="Selecciona la jornada",
            on_change=self._betting_week_changer,
            selected_index=selected_index,
            width=180,
        )

        responses_header = ft.Row(
            controls=[responses_title, self.dropdown],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        self.controls = [betting_title, form, divider, responses_header]

        self.controls.append(self.views[selected_index])

    def _betting_week_changer(self, event: ft.ControlEvent):
        self.controls = self.controls[:4]
        for i, (option, view) in enumerate(zip(self.options, self.views)):
            if option == event.data:
                self.controls.append(view)
                self.selected_index = i

        self.update()
