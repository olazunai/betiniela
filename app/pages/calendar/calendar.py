import flet as ft

from app.pages.calendar.calendar_create_match_modal import CalendarCreateMatchModal
from app.pages.calendar.calendar_week import CalendarWeek
from src.core.domain.dtos.data import Data
from src.core.domain.entities.user import UserRole


class Calendar(ft.Container):
    def __init__(self, data: Data):
        super().__init__()

        self.data: Data = data
        self.expand = True

    def build(self):
        self.selected_index = sorted(self.data.matches_by_week.matches.keys()).index(
            self.data.config.current_week.name()
        )
        self._build_function(self.selected_index)

    def did_mount(self):
        self.page.update()

    def before_update(self):
        self.data = self.page.data
        self._build_function(self.tabs.selected_index)

    def _build_function(self, selected_index: int):

        self.tabs = ft.Tabs(
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
                    content=CalendarWeek(matches_by_date=matches, user=self.data.user),
                )
                for option, matches in self.data.matches_by_week.matches.items()
            ],
            expand=True,
            scrollable=True,
            indicator_tab_size=True,
            splash_border_radius=ft.border_radius.all(20),
            label_padding=ft.padding.all(5),
        )

        self.content = ft.Stack(
            controls=[self.tabs],
            alignment=ft.alignment.bottom_left,
        )

        if self.data.user.role == UserRole.SUPERUSER:
            self.create_match = CalendarCreateMatchModal()
            self.content.controls.append(
                ft.Container(
                    ft.FloatingActionButton(
                        icon=ft.icons.ADD,
                        on_click=self._create_match_modal,
                    ),
                    alignment=ft.alignment.bottom_right,
                    height=50,
                    width=50,
                )
            )

    def _create_match_modal(self, e: ft.ControlEvent):
        self.page.open(self.create_match)
