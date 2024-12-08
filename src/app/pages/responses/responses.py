import flet as ft

from core.domain.dtos.data import Data


class Responses(ft.Container):
    def __init__(self, data: Data):
        super().__init__()
