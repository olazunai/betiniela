import flet as ft

from pages.betting.betting_form_week import BettingFormWeek
from pages.betting.betting_week import BettingWeek
from widgets.body import Body
from widgets.dropdown import Dropdown


class Betting(Body):
    def __init__(self, visible: bool, page: ft.Page):
        super().__init__(visible=visible)

        self.page = page

        form = BettingFormWeek()

        divider = ft.Divider()

        self.selected_index = 0

        self.options = [f"Jornada {i}" for i in range(30)]
        self.views = [BettingWeek(week=option, visible=i == self.selected_index) for i, option in enumerate(self.options)]
        
        dropdown = Dropdown(
            options=self.options,
            label="Selecciona la jornada",
            on_change=self._betting_week_changer,
            selected_index=self.selected_index,
        )

        self.controls = [form, divider, dropdown] + self.views

    def _betting_week_changer(self, event: ft. ControlEvent):
        for option, view in zip(self.options, self.views):
            if option == event.data:
                view.visible = True
            else:
                view.visible = False

        self.page.update()
    