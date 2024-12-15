from datetime import datetime
import flet as ft

from app.widgets.snack_bar import SnackBar
from src.core.application.config.config_updater_service import ConfigUpdaterService


class Configuration(ft.AlertDialog):
    def __init__(self):
        super().__init__()

        self.expand = True

    def build(self):
        self._build_function()

    def _build_function(self):
        self.current_week = ft.TextField(label="Jornada actual", expand=True)
        self.betting_limit = ft.TextField(
            label="Fecha y hora ('yyyy/mm/dd HH:MM:SS')", expand=True
        )
        self.right_winner_points = ft.TextField(
            label="Puntos por partido acertado", expand=True
        )
        self.right_losser_points = ft.TextField(
            label="Puntos extra por resultado aceptado", expand=True
        )
        self.started_week = ft.Checkbox(label="Jornada empezada", expand=True)

        editables = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        self.current_week,
                        ft.ElevatedButton(
                            "Editar",
                            on_click=self._change_current_week,
                        ),
                    ],
                    expand=True,
                ),
                ft.Row(
                    controls=[
                        self.betting_limit,
                        ft.ElevatedButton(
                            "Editar",
                            on_click=self._change_betting_limit,
                        ),
                    ],
                    expand=True,
                ),
                ft.Row(
                    controls=[
                        self.right_winner_points,
                        ft.ElevatedButton(
                            "Editar",
                            on_click=self._change_right_winner_points,
                        ),
                    ],
                    expand=True,
                ),
                ft.Row(
                    controls=[
                        self.right_losser_points,
                        ft.ElevatedButton(
                            "Editar",
                            on_click=self._change_right_losser_points,
                        ),
                    ],
                    expand=True,
                ),
                ft.Row(
                    controls=[
                        self.started_week,
                        ft.ElevatedButton(
                            "Editar",
                            on_click=self._change_started_week,
                        ),
                    ],
                    expand=True,
                ),
            ],
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        self.content = ft.Container(
            content=editables,
            width=500,
            alignment=ft.alignment.center,
            expand=True,
        )

    def _change_current_week(self, e: ft.ControlEvent) -> None:
        config_updater_service: ConfigUpdaterService = (
            self.page.container.services.config_updater_service
        )

        try:
            config_updater_service(current_week=self.current_week.value)
            success = True
            text = "Configuración actualizada correctamente"
        except Exception as e:
            success = False
            text = f"Ha ocurrido un error al actualizar la configuración: {e}"

        self.page.overlay.append(SnackBar(text=text, success=success, open=True))
        self.page.update()

    def _change_betting_limit(self, e: ft.ControlEvent) -> None:
        config_updater_service: ConfigUpdaterService = (
            self.page.container.services.config_updater_service
        )

        try:
            config_updater_service(
                betting_limit=datetime.strptime(
                    self.betting_limit.value, "%Y/%m/%d %H:%M:%S"
                )
            )
            success = True
            text = "Configuración actualizada correctamente"
        except Exception as e:
            success = False
            text = f"Ha ocurrido un error al actualizar la configuración: {e}"

        self.page.overlay.append(SnackBar(text=text, success=success, open=True))
        self.page.update()

    def _change_right_winner_points(self, e: ft.ControlEvent) -> None:
        config_updater_service: ConfigUpdaterService = (
            self.page.container.services.config_updater_service
        )

        try:
            config_updater_service(
                right_winner_points=int(self.right_winner_points.value)
            )
            success = True
            text = "Configuración actualizada correctamente"
        except Exception as e:
            success = False
            text = f"Ha ocurrido un error al actualizar la configuración: {e}"

        self.page.overlay.append(SnackBar(text=text, success=success, open=True))
        self.page.update()

    def _change_right_losser_points(self, e: ft.ControlEvent) -> None:
        config_updater_service: ConfigUpdaterService = (
            self.page.container.services.config_updater_service
        )

        try:
            config_updater_service(
                right_losser_points=int(self.right_losser_points.value)
            )

            success = True
            text = "Configuración actualizada correctamente"
        except Exception as e:
            success = False
            text = f"Ha ocurrido un error al actualizar la configuración: {e}"

        self.page.overlay.append(SnackBar(text=text, success=success, open=True))
        self.page.update()

    def _change_started_week(self, e: ft.ControlEvent) -> None:
        config_updater_service: ConfigUpdaterService = (
            self.page.container.services.config_updater_service
        )

        try:
            config_updater_service(
                started_week=self.started_week.value,
            )

            success = True
            text = "Configuración actualizada correctamente"
        except Exception as e:
            success = False
            text = f"Ha ocurrido un error al actualizar la configuración: {e}"

        self.page.overlay.append(SnackBar(text=text, success=success, open=True))
        self.page.update()
