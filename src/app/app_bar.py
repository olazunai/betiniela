import flet as ft

from app.configuration import Configuration
from core.domain.dtos.data import Data
from core.domain.entities.user import UserRole


class AppBar(ft.AppBar):
    def __init__(self, data: Data):
        super().__init__()

        self.data: Data = data

        self.leading = ft.Icon(ft.icons.PALETTE)
        self.leading_width = 40
        self.title = ft.Text("Betiniela")
        self.center_title = True

    def build(self):
        self._build_function()

    def _build_function(self):
        items = []
        if self.data.user.role == UserRole.SUPERUSER:
            items.append(
                ft.PopupMenuItem(
                    text="Configuración",
                    icon=ft.icons.SETTINGS,
                    on_click=self._settings,
                )
            )
            items.append(ft.PopupMenuItem())

        items.append(
            ft.PopupMenuItem(
                text="Cerrar sesión",
                icon=ft.icons.LOGOUT,
                on_click=self._logout,
            )
        )

        self.actions = [
            ft.PopupMenuButton(
                items=items,
                menu_position=ft.PopupMenuPosition.UNDER,
            ),
        ]

    def _logout(self, e: ft.ControlEvent):
        self.page.logout(e)

    def _settings(self, e: ft.ControlEvent):
        self.page.open(Configuration())
