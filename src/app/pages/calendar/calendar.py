import flet as ft

from pages.calendar.calendar_week import CalendarWeek
from widgets.body import Body


class Calendar(ft.Container):
    def __init__(self, visible: bool):
        super().__init__(visible=visible)

        self.expand = True

        self.options = [f"Jornada {i}" for i in range(30)]
        
        tabs = ft.Tabs(
            selected_index=1,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    tab_content=ft.Container(
                        content=ft.Text(option[0] + option.split()[-1]),
                        shape=ft.BoxShape.CIRCLE,
                        bgcolor=ft.colors.BLACK54,
                        width=50,
                        height=50,
                        alignment=ft.alignment.center,
                    ),
                    content=CalendarWeek(option),
                ) for option in self.options
            ],
            expand=True,
            scrollable=True,
            indicator_tab_size=True,
            splash_border_radius=ft.border_radius.all(20),
            label_padding=ft.padding.all(5),
        )

        self.content = tabs
    