import flet as ft

from app.widgets.body import Body
from app.pages.ranking.ranking_item import RankingItem


class Ranking(Body):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.page = page
        self.spacing = 2

        self.controls = [
            RankingItem(
                position=i, name=ranking.user_name.value, points=ranking.points.value
            )
            for i, ranking in enumerate(self.page.data.rankings, start=1)
        ]
