from datetime import datetime
import stat
import flet as ft

from widgets.body import Body
from pages.calendar.calendar_match import CalendarMatch


class CalendarWeek(ft.Column):
    def __init__(self, week: str):
        super().__init__()

        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.alignment = ft.CrossAxisAlignment.START
        self.scroll = ft.ScrollMode.HIDDEN

        self.controls = [
            self._get_day_text(datetime.now()),
            CalendarMatch(
                local_team="Altuna III - Aranguren",
                visitor_team="Jaka - Imaz",
                hour=datetime.now().time(),
            ),
            CalendarMatch(
                local_team="Artola - Mariezkurrena II",
                visitor_team="P. Etxeberria - Zabaleta",
                hour=datetime.now().time(),
            ),
            self._get_day_text(datetime.now()),
            CalendarMatch(
                local_team="Peña II - Albisu",
                visitor_team="Laso - Iztueta",
                hour=datetime.now().time(),
            ),
            self._get_day_text(datetime.now()),
            CalendarMatch(
                local_team="Peña II - Albisu",
                visitor_team="Laso - Iztueta",
                hour=datetime.now().time(),
            ),
        ]

    @staticmethod
    def _get_day_text(day: datetime) -> ft.Container:
        days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
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
            margin = ft.Margin(
                top=20,
                bottom=20,
                left=0,
                right=0,
            )
        )
