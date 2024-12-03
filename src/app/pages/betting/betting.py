import flet as ft

from app.pages.betting.betting_form_week import BettingFormWeek
from app.pages.betting.betting_week import BettingWeek
from app.widgets.body import Body
from app.widgets.dropdown import Dropdown
from core.domain.dtos.data import Data


class Betting(Body):
    def __init__(self, data: Data):
        super().__init__()

        weeks = sorted(data.matches_by_week.matches.keys())

        form = BettingFormWeek(
            week_name=weeks[0], data=data, show_form=not data.user.has_answered.value
        )

        divider = ft.Divider()

        self.selected_index = 0

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

        self.controls = [form, divider, dropdown] + self.views

    def _betting_week_changer(self, event: ft.ControlEvent):
        for option, view in zip(self.options, self.views):
            if option == event.data:
                view.visible = True
            else:
                view.visible = False

        self.page.update()
