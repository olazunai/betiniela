import flet as ft

from pages.betting.betting import Betting
from pages.calendar.calendar import Calendar
from pages.ranking.ranking import Ranking


class NavigationBar(ft.NavigationBar):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.page = page

        self.adaptive = True
        self.selected_index = 0
        self.animation_duration = 300

        self.destinations = [
            ft.NavigationBarDestination(label="Quiniela", icon=ft.icons.QUESTION_ANSWER_ROUNDED),
            ft.NavigationBarDestination(label="Clasificación", icon=ft.icons.FORMAT_LIST_BULLETED_OUTLINED),
            ft.NavigationBarDestination(label="Calendario", icon=ft.icons.CALENDAR_MONTH_OUTLINED),
            
        ]

        self.views = [
            Betting(visible=self.selected_index == 0, page=page),
            Ranking(visible=self.selected_index == 1),
            Calendar(visible=self.selected_index == 2),
        ]
        self.page.add(*self.views)

        self.on_change = self._page_changer

    def _page_changer(self, event: ft.ControlEvent):
        for i, view in enumerate(self.views):
            if i == int(event.data):
                view.visible = True
            else:
                view.visible = False

        self.page.update()
