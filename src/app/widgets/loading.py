import flet as ft


class Loading(ft.Container):
    def __init__(self):
        super().__init__()

        self.alignment = ft.alignment.center
        self.expand = True

        self.content = ft.ProgressRing(
            width = 25,
            height = 25,
            stroke_width = 3,
        )
