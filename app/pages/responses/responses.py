import flet as ft

from app.pages.responses.responses_all import ResponsesAll
from app.pages.responses.responses_user import ResponsesUser
from src.core.domain.dtos.data import Data


class Responses(ft.Container):
    def __init__(self, data: Data):
        super().__init__()
        
        self.data = data
        self.expand = True

    def build(self):
        self._build_function()

    def _build_function(self):
        self.tabs = ft.Tabs(
            animation_duration=300,
            tabs=[
                ft.Tab(
                    tab_content=ft.Container(
                        content=ft.Text("Tus respuestas"),
                        alignment=ft.alignment.center,
                    ),
                    content=ResponsesUser(data=self.data),
                ),
                ft.Tab(
                    tab_content=ft.Container(
                        content=ft.Text("Todas las respuestas"),
                        alignment=ft.alignment.center,
                    ),
                    content=ResponsesAll(data=self.data),
                )
            ],
            expand=True,
            indicator_tab_size=True,
            splash_border_radius=ft.border_radius.all(10),
            label_padding=ft.Padding(top=10, bottom=10, left=30, right=30),
            tab_alignment=ft.TabAlignment.CENTER,
            
        )
        self.content = self.tabs
