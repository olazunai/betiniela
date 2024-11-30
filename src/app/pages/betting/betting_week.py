import flet as ft

from pages.betting.betting_match import BettingMatch


class BettingWeek(ft.Container):
    def __init__(self, week: str, visible: bool):
        super().__init__()

        self.visible = visible

        self.content = ft.Column(
            controls=[
                BettingMatch(
                    local_team="Altuna III - Aranguren",
                    visitor_team="Jaka - Imaz",
                    winner="Altuna III - Aranguren",
                    losser="10-15",
                ),
                BettingMatch(
                    local_team="Artola - Mariezkurrena II",
                    visitor_team="P. Etxeberria - Zabaleta",
                    winner="P. Etxeberria - Zabaleta",
                    losser="10-15",
                ),
                BettingMatch(
                    local_team="Peña II - Albisu",
                    visitor_team="Laso - Iztueta",
                    winner="Peña II - Albisu",
                    losser="10-15",
                ),
                BettingMatch(
                    local_team="Peña II - Albisu",
                    visitor_team="Laso - Iztueta",
                    winner="Laso - Iztueta",
                    losser="10-15",
                )
            ]
        )
