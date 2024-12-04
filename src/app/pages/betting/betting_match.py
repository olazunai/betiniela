import flet as ft


class BettingMatch(ft.Container):
    def __init__(self, local_team: str, visitor_team: str, winner: str, losser: str):
        self.losser = losser
        super().__init__()

        header = ft.Row(
            controls=[
                ft.Container(content=ft.Divider(thickness=0.5), expand=True),
                ft.Text(
                    value=f"{local_team} vs {visitor_team}",
                    opacity=0.8,
                ),
                ft.Container(content=ft.Divider(thickness=0.5), expand=True),
            ],
            expand=True,
        )

        response = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(value=f"Ganador: {winner}", no_wrap=True),
                    ft.Text(value=f"Perdedor: {losser} tantos", no_wrap=True),
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                expand=True,
                spacing=30,
                wrap=True,
            ),
            alignment=ft.alignment.center,
            margin=ft.Margin(
                left=5,
                right=5,
                top=20,
                bottom=20,
            ),
            expand=True,
        )
        self.content = ft.Column(
            controls=[header, response],
        )
