import flet as ft

from app.pages.betting.betting_form_week import BettingFormWeek
from app.pages.betting.betting_week import BettingWeek
from app.widgets.body import Body
from app.widgets.dropdown import Dropdown
from core.domain.dtos.data import Data


class Betting(Body):
    def __init__(self, data: Data):
        super().__init__()

        self.data: Data = data

        weeks = sorted(data.matches_by_week.matches.keys())

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

        form = BettingFormWeek(week_name=weeks[0], data=data)

        divider = ft.Divider()

        responses_title = ft.Container(
            ft.Text(
                "Respuestas",
                text_align=ft.TextAlign.LEFT,
                size=20,
                theme_style=ft.TextThemeStyle.TITLE_SMALL,
                weight=ft.FontWeight.BOLD,
            ),
            margin=ft.margin.only(left=20, bottom=20),
        )

        self.selected_index = 0 if self.data.user.has_answered.value else None

        self.options = weeks
        self.views = [
            BettingWeek(week=option, visible=i == self.selected_index)
            for i, option in enumerate(self.options)
        ]

        dropdown = Dropdown(
            options=self.options,
            label="Selecciona la jornada",
            on_change=self._betting_week_changer,
            selected_index=self.selected_index,
        )

        responses_header = ft.Row(
            controls=[responses_title, dropdown],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        self.controls = [betting_title, form, divider, responses_header] + self.views

    def _betting_week_changer(self, event: ft.ControlEvent):
        for option, view in zip(self.options, self.views):
            if option == event.data:
                view.visible = True
            else:
                view.visible = False

        self.page.update()
