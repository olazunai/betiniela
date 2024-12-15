import flet as ft

from app.configuration import Configuration
from app.widgets.snack_bar import SnackBar
from constants import BAR_COLOR
from src.core.application.app.calculate_points_service import CalculatePointService
from src.core.domain.dtos.data import Data
from src.core.domain.entities.user import UserRole


class AppBar(ft.AppBar):
    def __init__(self, data: Data):
        super().__init__()

        self.data: Data = data

        self.title = ft.Text("Betiniela")
        self.center_title = True
        self.bgcolor = BAR_COLOR

    def build(self):
        self._build_function()

    def _build_function(self):
        items = []
        if self.data.user.role == UserRole.SUPERUSER:
            items.append(
                ft.PopupMenuItem(
                    text="Configuración",
                    icon=ft.Icons.SETTINGS,
                    on_click=self._settings,
                )
            )
            items.append(ft.PopupMenuItem())

        items.append(
            ft.PopupMenuItem(
                text="Cerrar sesión",
                icon=ft.Icons.LOGOUT,
                on_click=self._logout,
            )
        )

        self.actions = [
            ft.IconButton(icon=ft.Icons.REFRESH, on_click=self._refresh),
            ft.PopupMenuButton(
                items=items,
                menu_position=ft.PopupMenuPosition.UNDER,
            ),
        ]

        if self.data.user.role == UserRole.SUPERUSER:
            self.actions.insert(
                0,
                ft.IconButton(icon=ft.Icons.CALCULATE, on_click=self._calculate_points),
            )

    def _logout(self, e: ft.ControlEvent):
        self.page.logout(e)

    def _settings(self, e: ft.ControlEvent):
        self.page.open(Configuration())

    def _refresh(self, e: ft.ControlEvent):
        if self.page.controls:
            if self.page.controls[0].loading is not None:
                self.page.controls[0].loading.visible = True
                self.page.controls[0].loading.update()

        self.page.data = self.page.get_data(self.data.user)
        self.page.data.user = self.data.user
        self.page.update()

        if self.page.controls:
            if self.page.controls[0].loading is not None:
                self.page.controls[0].loading.visible = False
                self.page.controls[0].loading.update()

    def _calculate_points(self, e: ft.ControlEvent):
        calculate_points_service: CalculatePointService = (
            self.page.container.services.calculate_points_service
        )

        try:
            week_name = self.data.config.current_week.name()
            calculate_points_service(week_name=week_name)

            success = True
            text = "Puntos calculados correctamente"
        except Exception as e:
            success = False
            text = f"Ha ocurrido un error calculando los puntos: {e}"

        self.page.overlay.append(SnackBar(text=text, success=success, open=True))

        self.page.update()
