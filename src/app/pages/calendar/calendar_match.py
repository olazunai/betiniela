from datetime import datetime, time
import flet as ft


class CalendarMatch(ft.Container):
    def __init__(self, hour: time, local_team: str, visitor_team: str):
        super().__init__()

        self.margin = ft.Margin(
            left=10,
            right=10,
            top=2,
            bottom=2,
        )
        self.padding = ft.Padding(
            left=5,
            right=5,
            top=5,
            bottom=5,
        )
        self.border_radius = ft.border_radius.all(5)
        self.bgcolor = ft.colors.WHITE
        self.shape = ft.BoxShape.RECTANGLE
        self.width = 300
        self.alignment = ft.alignment.center
        self.width = 10000

        self.content = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text(
                        value=local_team,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.colors.BLACK,
                        weight=ft.FontWeight.BOLD,
                        no_wrap=True,
                    ),
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    content=ft.Text(
                        value=hour.strftime("%H:%mh"),
                        text_align=ft.TextAlign.CENTER,
                        color=ft.colors.BLACK,
                        weight=ft.FontWeight.BOLD,
                        no_wrap=True,
                    ),
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    content=ft.Text(
                        value=visitor_team,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.colors.BLACK,
                        weight=ft.FontWeight.BOLD,
                        no_wrap=True,
                    ),
                    alignment=ft.alignment.center,
                ),
            ],
            horizontal_alignment=ft.MainAxisAlignment.CENTER,
            spacing=2,
            tight=True,
        )
