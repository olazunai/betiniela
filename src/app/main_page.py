from typing import Callable
import flet as ft

from app.app_bar import AppBar
from app.navigation_bar import NavigationBar
from app.pages.betting.betting import Betting
from app.pages.calendar.calendar import Calendar
from app.pages.ranking.ranking import Ranking
from app.pages.responses.responses import Responses
from app.widgets.loading import Loading
from core.domain.dtos.data import Data
from core.application.app.auth_service import AuthService
from core.application.app.fetch_data_service import FetchDataService
from core.domain.entities.user import User


class MainPage(ft.Stack):
    def __init__(self, data: Data):
        super().__init__()

        self.expand = True
        self.data = data

    def build(self):
        self._build_function()

    def did_mount(self):
        self.loading.visible = False
        self.loading.update()

    def _build_function(self):
        self.page.save_token(user=self.data.user)

        self.page.appbar = AppBar(data=self.data)
        self.page.navigation_bar = NavigationBar(page_changer=self._page_changer)

        self.betting = Betting(data=self.data)
        self.responses = Responses(data=self.data)
        self.ranking = Ranking(data=self.data)
        self.calendar = Calendar(data=self.data)

        self.views = [self.betting, self.responses, self.ranking, self.calendar]
        self.loading = Loading()

        self.controls = [self.views[0], self.loading]

    def _page_changer(self, n_page: int):
        if len(self.controls) > 1:
            self.controls.pop(0)

        self.loading.visible = True
        self.update()

        self.controls.insert(0, self.views[n_page])

        self.update()

        self.loading.visible = False
        self.loading.update()
