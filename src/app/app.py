import flet as ft

from app.app_bar import AppBar
from app.navigation_bar import NavigationBar
from core.application.app.auth_service import AuthService
from core.application.app.fetch_data_service import FetchDataService
from core.domain.entities.user import User


class App(ft.Container):
    def __init__(self, user: User):
        super().__init__()

        self.user = user

    def build(self):
        self._build_function()

    def _build_function(self):
        fetch_data_service: FetchDataService = (
            self.page.container.services.fetch_data_service()
        )
        auth_service: AuthService = self.page.container.services.auth_service()

        data = fetch_data_service()
        data.user = self.user

        token = auth_service.generate_token(user=self.user)
        self.page.client_storage.set(key="betiniela.user_token", value=token)

        self.page.appbar = AppBar()
        self.page.navigation_bar = NavigationBar(data=data)
