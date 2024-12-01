import flet as ft


class Logo(ft.Text):
    def __init__(self, size: int):
        super().__init__()

        self.value = "Betiniela"
        self.text_align = ft.TextAlign.CENTER
        self.size = size
