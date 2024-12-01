import flet as ft

from app.login import Login
from app.app_bar import AppBar
from app.navigation_bar import NavigationBar


async def main(page: ft.Page):
    page.title = "Betiniela"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    login = Login(page=page)

    page.add(login)

    page.update()


if __name__ == "__main__":
    ft.app(main)
