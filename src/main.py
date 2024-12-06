from functools import partial
from typing import Optional
import flet as ft

from app.main_page import MainPage
from app.login import Login
from container import MainContainer
from core.application.app.auth_service import AuthService
from core.domain.entities.user import User


def check_token(page: ft.Page) -> Optional[User]:
    auth_service: AuthService = page.container.services.auth_service()

    token = page.client_storage.get("betiniela.user_token")
    if token is None:
        return None

    user = auth_service.validate_token(token=token)
    return user


def logout(page: ft.Page):
    page.client_storage.remove("betiniela.user_token")
    page.clean()
    page.add(Login())
    page.appbar = None
    page.navigation_bar = None
    page.update()


def main(page: ft.Page, container: MainContainer):
    page.title = "Betiniela"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    page.container = container
    page.logout = lambda x: logout(page)

    user = check_token(page)
    if user is not None:
        page.add(MainPage(user=user))
    else:
        page.add(Login())

    page.update()


if __name__ == "__main__":
    container = MainContainer()
    container.check_dependencies()
    container.init_resources()

    ft.app(partial(main, container=container))

    container.shutdown_resources()
