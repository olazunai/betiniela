import flet as ft

from core.application.match.match_deleter_service import MatchDeleterService
from core.domain.entities.match import MatchID


class CalendarDeleteMatchModal(ft.AlertDialog):
    def __init__(self, match_id: MatchID):
        super().__init__()

        self.expand = True

        self.match_id = match_id

        self.content = ft.Text("¿Seguro que quieres eliminar este partido?")
        self.actions = [
            ft.TextButton("Yes", on_click=self._delete_match),
            ft.TextButton("No", on_click=self._close),
        ]

    def _delete_match(self, e: ft.ControlEvent):
        match_deleter_service: MatchDeleterService = (
            self.page.container.services.match_deleter_service()
        )
        match_deleter_service(match_id=self.match_id.value)

    def _close(self, e: ft.ControlEvent):
        self.page.close(self)
