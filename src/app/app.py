import flet as ft

from app.app_bar import AppBar
from app.navigation_bar import NavigationBar
from app.pages.betting.betting import Betting
from app.pages.calendar.calendar import Calendar
from app.pages.ranking.ranking import Ranking
from app.widgets.loading import Loading
from core.domain.dtos.data import Data
from core.application.app.auth_service import AuthService
from core.application.app.fetch_data_service import FetchDataService
from core.domain.entities.user import User


class App(ft.Stack):
    def __init__(self, user: User):
        super().__init__()

        self.user = user
        self.expand = True

    def build(self):
        self._build_function()

    def did_mount(self):
        self.loading.visible = False

    def _build_function(self):
        fetch_data_service: FetchDataService = (
            self.page.container.services.fetch_data_service()
        )
        auth_service: AuthService = self.page.container.services.auth_service()

        data: Data = fetch_data_service()
        data.user = self.user

        token = auth_service.generate_token(user=self.user)
        self.page.client_storage.set(key="betiniela.user_token", value=token)

        self.page.appbar = AppBar()
        self.page.navigation_bar = NavigationBar(page_changer=self._page_changer)

        self.betting = Betting(data=data)
        self.ranking = Ranking(data=data)
        self.calendar = Calendar(data=data)

        self.views = [self.betting, self.ranking, self.calendar]
        self.loading = Loading()

        self.controls = [self.loading, self.views[0]]

    def _page_changer(self, n_page: int):
        if len(self.controls) > 1:
            self.controls.pop(-1)

        self.loading.visible = True
        self.update()

        self.controls.append(self.views[n_page])

        self.update()

        self.loading.visible = False
        self.loading.update()
