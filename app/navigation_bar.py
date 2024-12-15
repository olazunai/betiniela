from typing import Callable
import flet as ft


class NavigationBar(ft.NavigationBar):
    def __init__(self, page_changer: Callable):
        super().__init__()

        self.page_changer = page_changer

        self.adaptive = True
        self.animation_duration = 300

        self.destinations = [
            ft.NavigationBarDestination(
                label="Quiniela",
                icon=ft.Icons.QUESTION_MARK,
            ),
            ft.NavigationBarDestination(
                label="Respuestas", icon=ft.Icons.QUESTION_ANSWER_ROUNDED
            ),
            ft.NavigationBarDestination(
                label="Clasificación", icon=ft.Icons.FORMAT_LIST_BULLETED_OUTLINED
            ),
            ft.NavigationBarDestination(
                label="Calendario", icon=ft.Icons.CALENDAR_MONTH_OUTLINED
            ),
        ]

        self.on_change = self._page_changer

    def _page_changer(self, event: ft.ControlEvent):
        self.page_changer(int(event.data))
