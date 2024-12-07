from datetime import date, time
import flet as ft

from core.application.match.match_creator_service import MatchCreatorService
from core.application.match.match_updater_service import MatchUpdaterService
from core.domain.value_objects.team import Team


class CalendarCreateMatchModal(ft.AlertDialog):
    def __init__(self):
        super().__init__()

        self.expand = True

        self.week = ft.TextField(label="Semana", width=150)
        self.location = ft.TextField(label="Lugar", width=150)
        self.match_day = ft.TextField(label="Día ('yyyy-mm-dd')", expand=True)
        self.match_time = ft.TextField(label="Hora ('HH:MM:SS')", expand=True)

        teams = [team.value for team in Team]

        self.local_team = ft.Dropdown(
            options=[ft.dropdown.Option(team) for team in teams],
            label="Local team",
        )
        self.visitor_team = ft.Dropdown(
            options=[ft.dropdown.Option(team) for team in teams],
            label="Visitor team",
        )

        self.content = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=self.week,
                    ),
                    ft.Container(
                        content=self.location,
                    ),
                    ft.Container(
                        content=self.match_day,
                    ),
                    ft.Container(
                        content=self.match_time,
                    ),
                    ft.Container(
                        content=self.local_team,
                    ),
                    ft.Container(
                        content=self.visitor_team,
                    ),
                    ft.Container(
                        content=ft.ElevatedButton(
                            text="Crear",
                            on_click=self._create_match,
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
            height=450,
            width=350,
        )

    def _create_match(self, e: ft.ControlEvent):
        match_day = date.fromisoformat(self.match_day.value)
        match_time = time.fromisoformat(self.match_time.value)
        local_team = self.local_team.value
        visitor_team = self.visitor_team.value
        location = self.location.value
        week = self.week.value

        match_creator_service: MatchCreatorService = (
            self.page.container.services.match_creator_service()
        )
        match_creator_service(
            week=week,
            match_day=match_day,
            match_time=match_time,
            local_team=local_team,
            visitor_team=visitor_team,
            location=location,
        )
