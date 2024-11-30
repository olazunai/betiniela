from typing import Optional
import flet as ft


class Body(ft.Column):
    def __init__(self):
        super().__init__()

        self.expand = True
        self.alignment = ft.MainAxisAlignment.START
        self.scroll = ft.ScrollMode.HIDDEN
