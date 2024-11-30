import flet as ft


class RankingItem(ft.Container):
    def __init__(self, position: int, name: str, points: int):
        super().__init__()

        self.margin = ft.Margin(
            left=50,
            right=50,
            top=2,
            bottom=2,
        )
        self.padding = ft.padding.all(15)
        self.border_radius = ft.border_radius.all(5)
        self.bgcolor = ft.colors.BLACK54
        self.shape = ft.BoxShape.RECTANGLE

        self.content = ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(
                            value=position,
                            width=20,
                            text_align=ft.TextAlign.START,
                        ),
                        ft.Text(
                            value=name,
                            width=50,
                            text_align=ft.TextAlign.START,
                        ),
                    ],
                ),
                ft.Text(
                    value=str(points),
                    width=50,
                    text_align=ft.TextAlign.RIGHT,
                ),
            ],
            alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
        )