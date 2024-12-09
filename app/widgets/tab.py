from typing import Optional
import flet as ft


class Tab(ft.Tab):
    def __init__(self, text: str, icon: ft.Icon, content: Optional[ft.Control] = None):
        super().__init__()

        self.text = text
        self.icon = icon
        self.content = content
