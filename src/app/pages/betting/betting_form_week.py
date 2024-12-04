import flet as ft

from app.pages.betting.betting_form_match import BettingFormMatch
from core.application.response.response_creator_service import ResponseCreatorService
from core.application.user.user_has_answered_updater_service import (
    UserHasNasweredUpdaterService,
)
from core.domain.dtos.data import Data


class BettingFormWeek(ft.Container):
    def __init__(self, week_name: str, data: Data):
        super().__init__()

        self.week_name = week_name
        self.data: Data = data

    def build(self):
        self._build_function()

    def before_update(self):
        has_answered = self.data.user.has_answered.value
        self.no_form.visible = has_answered

    def _build_function(self):
        self.padding = ft.Padding(
            left=50,
            right=50,
            top=5,
            bottom=5,
        )

        self.no_form = ft.Container(
            content=ft.Text(
                "Ya has rellenado la quiniela de esta semana. Puedes editarla desde las respuestas.",
                visible=self.data.user.has_answered.value,
                text_align=ft.TextAlign.CENTER,
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.only(bottom=30)
        )
        self.pending_form = ft.Text(
            "Tienes pendiente una quiniela para rellenar",
            text_align=ft.TextAlign.CENTER,
            visible=not self.data.user.has_answered.value,
        )

        self.form_button = ft.Container(
            content=ft.ElevatedButton(
                text="Rellenar",
                on_click=self._form,
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.only(top=20, bottom=30),
            visible=not self.data.user.has_answered.value,
        )

        self.form_matches = []
        for matches in self.data.matches_by_week.matches[self.week_name].matches:
            for match in matches.matches:
                self.form_matches.append(
                    BettingFormMatch(
                        match_id=match.id,
                        local_team=match.local_team.value,
                        visitor_team=match.visitor_team.value,
                        visible=False,
                    )
                )

        self.submit_button = ft.ElevatedButton(
            text="Enviar respuesta", on_click=self._send_response, visible=False
        )

        self.content = ft.Column(
            controls=[self.no_form, self.pending_form, self.form_button]
            + self.form_matches
            + [self.submit_button],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    async def _send_response(self, event: ft.ControlEvent):
        response_creator_service: ResponseCreatorService = (
            self.page.container.services.response_creator_service()
        )
        user_has_answered_updater_service: UserHasNasweredUpdaterService = (
            self.page.container.services.user_has_answered_updater_service()
        )

        for form_match in self.form_matches:
            await response_creator_service(
                week_name=self.week_name,
                match_id=form_match.data.match_id.value,
                user_id=self.data.user.id.value,
                winner_team=form_match.data.winner,
                losser_points=form_match.data.losser,
            )

        await user_has_answered_updater_service(
            user_id=self.data.user.id.value,
            has_answered=True,
        )

        self.data.user.has_answered.value = True

        for form_match in self.form_matches:
            form_match.visible = False

        self.submit_button.visible = False

        self.update()

    async def _form(self, event: ft.ControlEvent):
        self.pending_form.visible = False
        self.form_button.visible = False

        for form_match in self.form_matches:
            form_match.visible = True

        self.submit_button.visible = True

        self.update()
