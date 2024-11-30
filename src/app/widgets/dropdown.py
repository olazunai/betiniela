import flet as ft

from typing import Callable


class Dropdown(ft.Container):
    def __init__(self, options: list[str], label: str, on_change: Callable, selected_index: int = None, text_size: int = None, label_size: int = None, width: int = 250):
        super().__init__()

        self.content=ft.Row(
            controls=[
                ft.Dropdown(
                    options=[ft.dropdown.Option(option) for option in options],
                    width=width,
                    label=label,
                    on_change=on_change,
                    value=options[selected_index] if selected_index is not None else None,
                    text_size=text_size,
                    label_style=ft.TextStyle(size=label_size)
                ),
            ],
            wrap=True,
        )