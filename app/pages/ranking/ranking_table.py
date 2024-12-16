import flet as ft

from src.core.domain.entities.ranking import Ranking


class RankingTable(ft.Container):
    def __init__(self, rankings: list[Ranking]):
        super().__init__()

        self.rankings: list[Ranking] = rankings
        self.sort_column_index = 2
        self.sort_ascending = False

    def build(self):
        self._build_function()

    def before_update(self):
        self._build_function()

    def _build_function(self):
        self.padding = ft.padding.only(top=10)
        self.data_table = ft.DataTable(
            sort_column_index=self.sort_column_index,
            sort_ascending=self.sort_ascending,
            columns=[
                ft.DataColumn(ft.Text(""), numeric=True),
                ft.DataColumn(ft.Text("")),
                ft.DataColumn(
                    ft.Text("Jor."), numeric=True, on_sort=self._sort_table_by_jor
                ),
                ft.DataColumn(
                    ft.Text("Tot."), numeric=True, on_sort=self._sort_table_by_tot
                ),
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
                        ft.DataCell(ft.Text(ranking.points.value)),
                        ft.DataCell(ft.Text(ranking.total_points.value)),
                        ft.DataCell(
                            ft.Text(
                                f"{ranking.right_winner.value}/{ranking.right_losser.value}"
                            )
                        ),
                        ft.DataCell(
                            ft.Text(
                                f"{ranking.total_right_winner.value}/{ranking.total_right_losser.value}"
                            )
                        ),
                    ],
                )
                for i, ranking in enumerate(self.rankings, start=1)
            ],
            data_row_max_height=float("inf"),
            column_spacing=15,
        )

        self.content = self.data_table

    def _sort_table_by_jor(self, e: ft.DataColumnSortEvent):
        self.rankings = sorted(
            self.rankings, reverse=not e.ascending, key=lambda x: x.points.value
        )
        self.sort_column_index = 2
        self.sort_ascending = e.ascending
        self.update()

    def _sort_table_by_tot(self, e: ft.DataColumnSortEvent):
        self.rankings = sorted(
            self.rankings, reverse=not e.ascending, key=lambda x: x.total_points.value
        )
        self.sort_column_index = 3
        self.sort_ascending = e.ascending
        self.update()
