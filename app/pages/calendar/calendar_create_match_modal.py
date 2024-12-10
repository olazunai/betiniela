from datetime import date, time
import flet as ft

from app.widgets.snack_bar import SnackBar
from src.core.application.match.match_creator_service import MatchCreatorService
from src.core.domain.value_objects.team import Team


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
            label="Local",
        )
        self.visitor_team = ft.Dropdown(
            options=[ft.dropdown.Option(team) for team in teams],
            label="Visitante",
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
            self.page.container.services.match_creator_service
        )
        try:
            match_creator_service(
                week=week,
                match_day=match_day,
                match_time=match_time,
                local_team=local_team,
                visitor_team=visitor_team,
                location=location,
            )
            success = True
            text = "Partido creado correctamente"
        except Exception as e:
            success = False
            text = f"Ha ocurrido un error al crear el partido: {e}"

        self.page.close(self)

        self.page.overlay.append(SnackBar(text=text, success=success, open=True))
        self.page.update()
