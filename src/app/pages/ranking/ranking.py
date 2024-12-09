from app.widgets.body import Body
from app.pages.ranking.ranking_item import RankingItem
from core.domain.dtos.data import Data


class Ranking(Body):
    def __init__(self, data: Data):
        super().__init__()

        self.spacing = 2
        self.data = data

    def build(self):
        self._build_function()

    def before_update(self):
        self.data = self.page.data
        self._build_function()

    def _build_function(self):
        self.controls = [
            RankingItem(
                position=i, name=ranking.user_name.value, points=ranking.points.value
            )
            for i, ranking in enumerate(self.data.rankings, start=1)
        ]
