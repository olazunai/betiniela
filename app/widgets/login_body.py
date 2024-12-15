import flet as ft


class LoginBody(ft.Container):
    def __init__(self):
        super().__init__()

        self.border_radius = 20
        self.width = 320
        self.height = 450
        self.bgcolor = ft.Colors.BLACK38

        self.padding = ft.padding.all(20)
