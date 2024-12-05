import flet as ft

from app.pages.betting.betting import Betting
from app.pages.calendar.calendar import Calendar
from app.pages.ranking.ranking import Ranking
from core.domain.dtos.data import Data


class NavigationBar(ft.NavigationBar):
    def __init__(self, data: Data):
        super().__init__()

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

        self.betting = Betting(data=data)
        self.ranking = Ranking(data=data)
        self.calendar = Calendar(data=data)

        self.views = [self.betting, self.ranking, self.calendar]

        self.on_change = self._page_changer

    def build(self):
        self.page.controls.append(self.views[self.selected_index])

    def did_mount(self):
        self.page.update()

    def _page_changer(self, event: ft.ControlEvent):
        self.page.remove_at(-1)
        self.page.add(self.views[int(event.data)])

        self.page.update()
