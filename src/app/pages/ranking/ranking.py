from app.widgets.body import Body
from app.pages.ranking.ranking_item import RankingItem
from core.domain.dtos.data import Data


class Ranking(Body):
    def __init__(self, data: Data):
        super().__init__()

        self.spacing = 2

        self.controls = [
            RankingItem(
                position=i, name=ranking.user_name.value, points=ranking.points.value
            )
            for i, ranking in enumerate(data.rankings, start=1)
        ]
