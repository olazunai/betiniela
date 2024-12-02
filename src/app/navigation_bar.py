import flet as ft

from app.pages.betting.betting import Betting
from app.pages.calendar.calendar import Calendar
from app.pages.ranking.ranking import Ranking


class NavigationBar(ft.NavigationBar):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.page = page

        self.adaptive = True
        self.selected_index = 0
        self.animation_duration = 300

        self.destinations = [
            ft.NavigationBarDestination(
                label="Quiniela", icon=ft.icons.QUESTION_ANSWER_ROUNDED
            ),
            ft.NavigationBarDestination(
                label="Clasificación", icon=ft.icons.FORMAT_LIST_BULLETED_OUTLINED
            ),
            ft.NavigationBarDestination(
                label="Calendario", icon=ft.icons.CALENDAR_MONTH_OUTLINED
            ),
        ]

        self.views = [
            Betting(page=page),
            Ranking(page=page),
            Calendar(page=page),
        ]
        self.page.add(self.views[self.selected_index])

        self.on_change = self._page_changer

    def _page_changer(self, event: ft.ControlEvent):
        self.page.remove_at(0)
        self.page.add(self.views[int(event.data)])

        self.page.update()
