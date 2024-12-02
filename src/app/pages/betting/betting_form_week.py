import flet as ft

from app.pages.betting.betting_form_match import BettingFormMatch
from core.application.response.response_creator_service import ResponseCreatorService


class BettingFormWeek(ft.Container):
    def __init__(self, week_name: str, page: ft.Page):
        super().__init__()

        self.week_name = week_name

        self.padding = ft.Padding(
            left=50,
            right=50,
            top=5,
            bottom=5,
        )

        self.controls = []
        for matches in page.data.matches_by_week.matches[week_name].matches:
            for match in matches.matches:
                self.controls.append(
                    BettingFormMatch(
                        match_id=match.id,
                        local_team=match.local_team.value,
                        visitor_team=match.visitor_team.value,
                    )
                )

        self.submit_button = ft.ElevatedButton(
            text="Enviar respuesta", on_click=self._send_response
        )

        self.content = ft.Column(
            controls=self.controls + [self.submit_button],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    async def _send_response(self, event: ft.ControlEvent):
        response_creator_service: ResponseCreatorService = (
            self.page.container.services.response_creator_service()
        )

        for control in self.controls:
            await response_creator_service(
                week_name=self.week_name,
                match_id=control.data.match_id.value,
                user_id=self.page.user.id.value,
                winner_team=control.data.winner,
                losser_points=control.data.losser,
            )
