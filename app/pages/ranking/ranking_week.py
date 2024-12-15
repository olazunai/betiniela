from textwrap import wrap
import flet as ft

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

        self.data_table = ft.Container(
            content=ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text(""), numeric=True),
                    ft.DataColumn(ft.Text("")),
                    ft.DataColumn(ft.Text("Tot."), numeric=True),
                    ft.DataColumn(ft.Text("Jor."), numeric=True),
                    ft.DataColumn(ft.Text("+"), numeric=True),
                    ft.DataColumn(
                        ft.Text("++", tooltip=ft.Tooltip(message="Tanteo acertado")),
                        numeric=True,
                    ),
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(i)),
                            ft.DataCell(
                                ft.Container(
                                    content=ft.Text(
                                        ranking.user_name.value,
                                        overflow=ft.TextOverflow.ELLIPSIS,
                                    ),
                                    width=120,
                                )
                            ),
                            ft.DataCell(ft.Text(ranking.total_points.value)),
                            ft.DataCell(ft.Text(ranking.points.value)),
                            ft.DataCell(
                                ft.Text(
                                    f"{ranking.total_right_winner.value}/{ranking.total_right_losser.value}"
                                )
                            ),
                            ft.DataCell(
                                ft.Text(
                                    f"{ranking.right_winner.value}/{ranking.right_losser.value}"
                                )
                            ),
                        ],
                    )
                    for i, ranking in enumerate(week_rankings, start=1)
                ],
                data_row_max_height=float("inf"),
                column_spacing=15,
            ),
            padding=ft.padding.only(top=50),
        )

        self.no_data = ft.Container(
            content=ft.Text(
                "Ranking no disponible para esta semana.",
                text_align=ft.TextAlign.CENTER,
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.only(top=20),
        )

        if week_rankings:
            self.content = self.data_table

        else:
            self.content = self.no_data
