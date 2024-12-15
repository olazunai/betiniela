import flet as ft


class SnackBar(ft.SnackBar):
    def __init__(self, text: str = "", success: bool = True, open: bool = False):
        super().__init__(ft.Text(text))

        self.text = text
        self.open = open
        self.success = success

    def build(self):
        self._build_function()

    def _build_function(self):
        self.bgcolor = ft.Colors.GREEN if self.success else ft.Colors.RED
        self.behavior = ft.SnackBarBehavior.FLOATING
        self.duration = 2500

        self.content = ft.Text(self.text)

        self.show_close_icon = True
