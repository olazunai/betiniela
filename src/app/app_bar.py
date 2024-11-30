import flet as ft


class AppBar(ft.AppBar):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.page = page

        self.adaptive = True
        self.leading = ft.Icon(ft.icons.PALETTE)
        self.leading_width = 40
        self.title = ft.Text("Betiniela")
        self.center_title = True

        self.actions = [
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="Item 1"),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(
                        text="Checked item", checked=False, on_click=self._item_clicker
                    ),
                ],
                menu_position=ft.PopupMenuPosition.UNDER,
            ),
        ]

    def _item_clicker(self, event: ft.ControlEvent):
        event.control.checked = not event.control.checked
        self.page.update()