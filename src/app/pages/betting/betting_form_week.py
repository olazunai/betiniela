import flet as ft

from pages.betting.betting_form_match import BettingFormMatch


class BettingFormWeek(ft.Container):
    def __init__(self):
        super().__init__()

        self.padding = ft.Padding(
            left=50,
            right=50,
            top=5,
            bottom=5,
        )

        match_1 = BettingFormMatch(
            local_team="Altuna III - Aranguren",
            visitor_team="Jaka - Imaz",
        )
        match_2 = BettingFormMatch(
            local_team="Peña II - Albisu",
            visitor_team="Laso - Iztueta",
        )
        match_3 = BettingFormMatch(
            local_team="Artola - Mariezkurrena II",
            visitor_team="P. Etxeberria - Zabaleta",
        )
        match_4 = BettingFormMatch(
            local_team="Peña II - Albisu",
            visitor_team="Laso - Iztueta",
        )

        divider = ft.Divider(thickness=0.5)

        self.content = ft.Column(
            controls=[divider, match_1, divider, match_2, divider, match_3, divider, match_4],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
        )
