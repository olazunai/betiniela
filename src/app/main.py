import flet as ft

from app_bar import AppBar
from navigation_bar import NavigationBar


async def main(page: ft.Page):
    page.title = "Betiniela"

    page.appbar = AppBar(page=page)
    page.navigation_bar = NavigationBar(page=page)

    page.update()


if __name__ == "__main__":
    ft.app(main)
