from functools import partial
import flet as ft

from app.login import Login
from container import MainContainer


def main(page: ft.Page, container: MainContainer):
    page.title = "Betiniela"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    page.container = container

    page.add(Login())

    page.update()


if __name__ == "__main__":
    container = MainContainer()
    container.check_dependencies()
    container.init_resources()

    ft.app(partial(main, container=container))

    container.shutdown_resources()
