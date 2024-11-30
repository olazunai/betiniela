import flet as ft


class Body(ft.Column):
    def __init__(self, visible: bool):
        super().__init__()

        self.visible = visible
        self.expand = True
        self.alignment = ft.MainAxisAlignment.START
        self.scroll = ft.ScrollMode.ADAPTIVE
