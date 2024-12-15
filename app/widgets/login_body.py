import flet as ft

from constants import SECONDARY_COLOR


class LoginBody(ft.Container):
    def __init__(self):
        super().__init__()

        self.border_radius = 20
        self.width = 320
        self.height = 450
        self.bgcolor = SECONDARY_COLOR

        self.padding = ft.padding.all(20)
