from datetime import datetime
import flet as ft

from app.pages.calendar.calendar_match import CalendarMatch
from core.domain.dtos.matches_by_week import MatchesByDate
from core.domain.entities.user import User


class CalendarWeek(ft.Column):
    def __init__(self, matches_by_date: MatchesByDate, user: User):
        super().__init__()

        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.alignment = ft.CrossAxisAlignment.START
        self.scroll = ft.ScrollMode.HIDDEN
        self.user = user

        self.controls = []
        for matches in matches_by_date.matches:
            self.controls.append(self._get_day_text(matches.day))
            for match in matches.matches:
                self.controls.append(
                    CalendarMatch(
                        match_id=match.id,
                        local_team=match.local_team.value,
                        visitor_team=match.visitor_team.value,
                        hour=match.match_time,
                        result=match.result,
                        user=user,
                    )
                )

    @staticmethod
    def _get_day_text(day: datetime) -> ft.Container:
        days = [
            "Lunes",
            "Martes",
            "Miércoles",
            "Jueves",
            "Viernes",
            "Sábado",
            "Domingo",
        ]
        months = [
            "enero",
            "febrero",
            "Marzo",
            "abril",
            "mayo",
            "junio",
            "julio",
            "agosto",
            "septiembre",
            "octubre",
            "noviembre",
            "diciembre",
        ]
        value = f"{days[day.weekday()]}, {day.day} de {months[day.month - 1]}"
        return ft.Container(
            content=ft.Text(value, text_align=ft.TextAlign.CENTER, size=20),
            margin=ft.Margin(
                top=20,
                bottom=20,
                left=0,
                right=0,
            ),
        )
