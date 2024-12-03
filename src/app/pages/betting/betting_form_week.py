import flet as ft

from app.pages.betting.betting_form_match import BettingFormMatch
from core.application.response.response_creator_service import ResponseCreatorService
from core.application.user.user_has_answered_updater_service import (
    UserHasNasweredUpdaterService,
)
from core.domain.dtos.data import Data


class BettingFormWeek(ft.Container):
    def __init__(self, week_name: str, data: Data, show_form: bool):
        super().__init__()

        self.week_name = week_name
        self.data = data

        self.padding = ft.Padding(
            left=50,
            right=50,
            top=5,
            bottom=5,
        )

        self.no_form = ft.Text(
            "Ya has rellenado la quiniela de esta semana. Puedes editarla desde las respuestas.",
            visible=not show_form,
        )
        self.to_answer = ft.Text("Tienes pendiente una quiniela para rellenar")
        self.form_button = ft.ElevatedButton(text="Rellenar", on_click=self._form)

        self.controls = []
        for matches in data.matches_by_week.matches[week_name].matches:
            for match in matches.matches:
                self.controls.append(
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
            controls=[self.no_form, self.to_answer, self.form_button]
            + self.controls
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

        for control in self.controls:
            await response_creator_service(
                week_name=self.week_name,
                match_id=control.data.match_id.value,
                user_id=self.data.user.id.value,
                winner_team=control.data.winner,
                losser_points=control.data.losser,
            )

        await user_has_answered_updater_service(
            user_id=self.data.user.id.value,
            has_answered=True,
        )

        self.data.user.has_answered.value = True

        self.no_form.visible = True

        for control in self.controls:
            control.visible = False

        self.submit_button.visible = False

        self.page.update()

    async def _form(self, event: ft.ControlEvent):
        self.to_answer.visible = False
        self.form_button.visible = False

        for control in self.controls:
            control.visible = True

        self.submit_button.visible = True

        self.page.update()
