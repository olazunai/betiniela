from datetime import datetime
import flet as ft

from app.pages.betting.betting_week import BettingWeek
from app.utils import is_week_started
from src.core.application.user.user_retriever_service import UserRetrieverService
from src.core.domain.entities.user import User, UserRole
from src.core.domain.entities.match import Match
from src.core.domain.dtos.data import Data


class Betting(ft.Container):
    def __init__(self, data: Data):
        super().__init__()

        self.data: Data = data
        self.week_name = self.data.config.current_week.name()

        self.user: User = self.data.user
        self.no_available = is_week_started(data=self.data, week_name=self.week_name)

    def build(self):
        self._build_function()

    def before_update(self):
        user_retriever_service: UserRetrieverService = (
            self.page.container.services.user_retriever_service
        )

        self.user = user_retriever_service(self.user.id.value)
        self.data.user = self.user

        self.no_available = is_week_started(data=self.data, week_name=self.week_name)
        self._build_function()

    def _build_function(self):
        self.padding = ft.Padding(
            left=50,
            right=50,
            top=5,
            bottom=5,
        )
        self.has_answered = self.user.has_answered.value

        self.answered_form = ft.Container(
            content=ft.Text(
                "Ya has rellenado la quiniela de esta semana. Puedes editarla desde las respuestas.",
                text_align=ft.TextAlign.CENTER,
                expand=True,
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.only(bottom=30, left=50, right=50),
            visible=self.has_answered and not self.no_available,
            expand=True,
        )
        self.no_form = ft.Container(
            content=ft.Text(
                "La jornada ya ha empezado y no se pueden cambiar las respuestas.",
                text_align=ft.TextAlign.CENTER,
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.only(bottom=30, left=50, right=50),
            visible=self.no_available,
        )

        self.form = BettingWeek(
            week_name=self.week_name,
            data=self.data,
            visible=not self.has_answered and not self.no_available,
        )

        self.content = ft.Column(
            controls=[self.answered_form, self.no_form, self.form],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
