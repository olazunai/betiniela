import flet as ft

from app.pages.ranking.ranking_table import RankingTable
from src.core.domain.entities.ranking import Ranking
from src.core.domain.value_objects.week import Week
from src.core.domain.dtos.data import Data


class RankingWeek(ft.Container):
    def __init__(self, data: Data, week: Week):
        super().__init__()

        self.data: Data = data
        self.week: Week = week

    def build(self):
        self._build_function()

    def before_update(self):
        self.data = self.page.data
        self._build_function()

    def _build_function(self):
        week_rankings: list[Ranking] = [
            ranking for ranking in self.data.rankings if ranking.week == self.week
        ]

        self.info = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("+: Aciertos jornada (partido / tanteo)"),
                    ft.Text("++: Total aciertos (partido / tanteo)"),
                ]
            ),
            padding=ft.padding.only(top=40, left=10),
        )

        self.no_data = ft.Container(
            content=ft.Text(
                "Ranking no disponible para esta semana.",
                text_align=ft.TextAlign.CENTER,
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.only(top=80),
        )

        if week_rankings:
            self.content = ft.Column(
                controls=[self.info, RankingTable(rankings=week_rankings)]
            )

        else:
            self.content = self.no_data
