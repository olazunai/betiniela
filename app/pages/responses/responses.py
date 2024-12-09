import flet as ft

from src.core.domain.dtos.data import Data


class Responses(ft.Container):
    def __init__(self, data: Data):
        super().__init__()
