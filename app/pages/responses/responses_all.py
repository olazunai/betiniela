import flet as ft

from app.pages.responses.responses_user_week import ResponsesUserWeek
from app.widgets.body import Body
from app.widgets.dropdown import Dropdown
from src.core.domain.dtos.data import Data
from src.core.domain.value_objects.week import Week


class ResponsesAll(Body):
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

        self.options = self.weeks
        self.views = [
            ResponsesUserWeek(week=Week.deserialize(option), data=self.data, visible=True)
            for option in self.options
        ]

        self.dropdown = Dropdown(
            options=self.options,
            label="Selecciona la jornada",
            on_change=self._week_changer,
            selected_index=selected_index,
            width=180,
        )

        week_dropdown = ft.Container(
            content=self.dropdown,
            padding=ft.Padding(top=50, left=5, right=5, bottom=10)
        )

        self.controls = [week_dropdown]

        self.controls.append(self.views[selected_index])

    def _week_changer(self, event: ft.ControlEvent):
        self.controls = self.controls[:4]
        for i, (option, view) in enumerate(zip(self.options, self.views)):
            if option == event.data:
                self.controls.append(view)
                self.selected_index = i

        self.update()
