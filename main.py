from functools import partial
from typing import Optional
import flet as ft

from app.main_page import MainPage
from app.login import Login
from constants import PRIMARY_COLOR
from container import MainContainer
from src.core.application.user.user_retriever_service import UserRetrieverService
from src.core.application.app.auth_service import AuthService
from src.core.application.app.fetch_data_service import FetchDataService
from src.core.domain.dtos.data import Data
from src.core.domain.entities.user import User


def check_token(page: ft.Page) -> Optional[User]:
    auth_service: AuthService = page.container.services.auth_service

    token = page.client_storage.get("betiniela.user_token")
    if token is None:
        return None

    user = auth_service.validate_token(token=token)
    return user


def save_token(user: User, page: ft.Page) -> None:
    auth_service: AuthService = page.container.services.auth_service
    token = auth_service.generate_token(user=user)
    page.client_storage.set(key="betiniela.user_token", value=token)


def logout(page: ft.Page):
    page.client_storage.remove("betiniela.user_token")
    page.clean()
    page.add(Login())
    page.appbar = None
    page.navigation_bar = None
    page.update()


def get_data(user: User, page: ft.Page) -> Data:
    fetch_data_service: FetchDataService = page.container.services.fetch_data_service
    user_retriever_service: UserRetrieverService = (
        page.container.services.user_retriever_service
    )

    data: Data = fetch_data_service()
    page.data = data
    data.user = user_retriever_service(user.id.value)
    return data


def init_main_page(user: User, page: ft.Page) -> MainPage:
    data = page.get_data(user=user)
    return MainPage(data=data)


def main(page: ft.Page, container: MainContainer):
    page.title = "Betiniela"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = PRIMARY_COLOR

    page.container = container
    page.logout = lambda x: logout(page=page)
    page.save_token = partial(save_token, page=page)
    page.get_data = partial(get_data, page=page)
    page.init_main_page = partial(init_main_page, page=page)

    user = check_token(page)
    if user is not None:
        page.add(page.init_main_page(user))
    else:
        page.add(Login())

    page.update()


if __name__ == "__main__":
    container = MainContainer()

    ft.app(partial(main, container=container), assets_dir="assets")
