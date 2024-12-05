import flet as ft


class WindowDrag(ft.Container):
    def __init__(self):
        super().__init__()

        self.content = ft.WindowDragArea(
            height=50, content=ft.Container(bgcolor="white")
        )
