import flet as ft

from widgets.body import Body
from pages.ranking.ranking_item import RankingItem


class Ranking(Body):
    def __init__(self, visible: bool):
        super().__init__(visible=visible)

        self.spacing = 2

        ranking_data = [
            {"nombre": "Juan", "puntos": 2500},
            {"nombre": "Ana", "puntos": 2300},
            {"nombre": "Luis", "puntos": 2100},
            {"nombre": "Marta", "puntos": 1800},
            {"nombre": "Carlos", "puntos": 1700},
            {"nombre": "Pedro", "puntos": 1500},
            {"nombre": "Sofía", "puntos": 1400},
            {"nombre": "Juan", "puntos": 2500},
            {"nombre": "Ana", "puntos": 2300},
            {"nombre": "Luis", "puntos": 2100},
            {"nombre": "Marta", "puntos": 1800},
            {"nombre": "Carlos", "puntos": 1700},
            {"nombre": "Pedro", "puntos": 1500},
            {"nombre": "Sofía", "puntos": 1400},
            {"nombre": "Juan", "puntos": 2500},
            {"nombre": "Ana", "puntos": 2300},
            {"nombre": "Luis", "puntos": 2100},
            {"nombre": "Marta", "puntos": 1800},
            {"nombre": "Carlos", "puntos": 1700},
            {"nombre": "Pedro", "puntos": 1500},
            {"nombre": "Sofía", "puntos": 1400},
            {"nombre": "Juan", "puntos": 2500},
            {"nombre": "Ana", "puntos": 2300},
            {"nombre": "Luis", "puntos": 2100},
            {"nombre": "Marta", "puntos": 1800},
            {"nombre": "Carlos", "puntos": 1700},
            {"nombre": "Pedro", "puntos": 1500},
            {"nombre": "Sofía", "puntos": 1400},
        ]

        self.controls = [
            RankingItem(position=i, name=player["nombre"], points=player["puntos"]) for i, player in enumerate(ranking_data, start=1)
        ]
