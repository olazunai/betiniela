import flet as ft

from app.pages.calendar.calendar_week import CalendarWeek
from core.domain.dtos.data import Data


class Calendar(ft.Container):
    def __init__(self, data: Data):
        super().__init__()

        self.data: Data = data
        self.expand = True

    def build(self):
        self._build_function()

    def _build_function(self):
        selected_index = sorted(self.data.matches_by_week.matches.keys()).index(
            self.data.config.current_week.name()
        )
        tabs = ft.Tabs(
            selected_index=selected_index,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    tab_content=ft.Container(
                        content=ft.Text(option[0].capitalize() + option.split()[-1]),
                        shape=ft.BoxShape.CIRCLE,
                        bgcolor=ft.colors.BLACK54,
                        width=50,
                        height=50,
                        alignment=ft.alignment.center,
                    ),
                    content=CalendarWeek(matches),
                )
                for option, matches in self.data.matches_by_week.matches.items()
            ],
            expand=True,
            scrollable=True,
            indicator_tab_size=True,
            splash_border_radius=ft.border_radius.all(20),
            label_padding=ft.padding.all(5),
        )

        self.content = tabs
