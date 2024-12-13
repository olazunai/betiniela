from datetime import time
import flet as ft

from app.widgets.snack_bar import SnackBar
from src.core.application.match.match_updater_service import MatchUpdaterService
from src.core.domain.entities.match import Match
from src.core.domain.value_objects.team import Team


class CalendarEditMatchModal(ft.AlertDialog):
    def __init__(self, match: Match):
        super().__init__()

        self.expand = True

        self.match = match

        self.match_time = ft.TextField(
            label="Hora ('HH:MM:SS')",
            value=self.match.match_time.isoformat(),
            width=150,
        )

        teams = [team.value for team in Team]

        self.local_team = ft.Dropdown(
            options=[ft.dropdown.Option(team) for team in teams],
            label="Local",
            value=self.match.local_team.value,
        )
        self.visitor_team = ft.Dropdown(
            options=[ft.dropdown.Option(team) for team in teams],
            label="Visitante",
            value=self.match.visitor_team.value,
        )
        self.local_team_result = ft.TextField(
            width=50,
            value=(
                self.match.result.local_team if self.match.result is not None else None
            ),
        )
        self.visitor_team_result = ft.TextField(
            width=50,
            value=(
                self.match.result.visitor_team
                if self.match.result is not None
                else None
            ),
        )

        self.content = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=self.match_time,
                    ),
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=self.local_team,
                            ),
                            ft.Container(
                                content=ft.Text(value="-"),
                            ),
                            ft.Container(
                                content=self.local_team_result,
                            ),
                        ],
                    ),
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=self.visitor_team,
                            ),
                            ft.Container(
                                content=ft.Text(value="-"),
                            ),
                            ft.Container(
                                content=self.visitor_team_result,
                            ),
                        ],
                    ),
                    ft.Container(
                        content=ft.ElevatedButton(
                            text="Actualizar",
                            on_click=self._update_match,
                        ),
                    ),
                ],
                horizontal_alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                spacing=10,
                tight=True,
                expand=True,
            ),
            expand=True,
            height=350,
            width=350,
        )

    def _update_match(self, e: ft.ControlEvent):
        match_time = time.fromisoformat(self.match_time.value)
        local_team = self.local_team.value
        visitor_team = self.visitor_team.value
        local_team_result = int(self.local_team_result.value)
        visitor_team_result = int(self.visitor_team_result.value)

        match_updater_service: MatchUpdaterService = (
            self.page.container.services.match_updater_service
        )
        try:
            match_updater_service(
                match_id=self.match.id.value,
                match_time=match_time,
                local_team=local_team,
                visitor_team=visitor_team,
                local_team_result=local_team_result,
                visitor_team_result=visitor_team_result,
            )
            success = True
            text = "Partido editado correctamente"
        except Exception as e:
            success = False
            text = f"Ha ocurrido un error al editar el partido: {e}"

        self.page.close(self)

        self.page.overlay.append(SnackBar(text=text, success=success, open=True))
        self.page.update()
