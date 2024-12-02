import asyncio
import flet as ft

from app.pages.calendar.calendar_week import CalendarWeek
from core.domain.entities.match import Match


class Calendar(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.page = page

        self.expand = True

        tabs = ft.Tabs(
            selected_index=1,
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
                for option, matches in self.page.data.matches_by_week.matches.items()
            ],
            expand=True,
            scrollable=True,
            indicator_tab_size=True,
            splash_border_radius=ft.border_radius.all(20),
            label_padding=ft.padding.all(5),
        )

        self.content = tabs
