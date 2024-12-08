from datetime import time
from typing import Optional
import flet as ft

from app.pages.calendar.calendar_delete_match_modal import CalendarDeleteMatchModal
from app.pages.calendar.calendar_edit_match_modal import CalendarEditMatchModal
from core.domain.entities.match import MatchID, MatchResult
from core.domain.entities.user import User, UserRole


class CalendarMatch(ft.Container):
    def __init__(
        self,
        hour: time,
        match_id: MatchID,
        local_team: str,
        visitor_team: str,
        user: User,
        result: Optional[MatchResult] = None,
    ):
        super().__init__()

        self.match_id = match_id

        self.margin = ft.Margin(
            left=10,
            right=10,
            top=2,
            bottom=2,
        )
        self.padding = ft.Padding(
            left=5,
            right=5,
            top=5,
            bottom=5,
        )
        self.border_radius = ft.border_radius.all(5)
        self.bgcolor = ft.colors.WHITE
        self.shape = ft.BoxShape.RECTANGLE
        self.width = 300
        self.alignment = ft.alignment.center
        self.width = 10000

        match_content = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text(
                        value=local_team,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.colors.BLACK,
                        weight=ft.FontWeight.BOLD,
                        no_wrap=True,
                    ),
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    content=ft.Text(
                        value=(
                            hour.strftime("%H:%Mh")
                            if result is None
                            else f"{result.local_team} - {result.visitor_team}"
                        ),
                        text_align=ft.TextAlign.CENTER,
                        color=ft.colors.BLACK,
                        weight=ft.FontWeight.BOLD,
                        no_wrap=True,
                    ),
                    alignment=ft.alignment.center,
                ),
                ft.Container(
                    content=ft.Text(
                        value=visitor_team,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.colors.BLACK,
                        weight=ft.FontWeight.BOLD,
                        no_wrap=True,
                    ),
                    alignment=ft.alignment.center,
                ),
            ],
            horizontal_alignment=ft.MainAxisAlignment.CENTER,
            spacing=2,
            tight=True,
            expand=True,
        )

        self.content = ft.Row(
            controls=[match_content],
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        if user.role == UserRole.SUPERUSER:
            self.edit_match = CalendarEditMatchModal(
                match_id=self.match_id,
                hour=hour,
                local_team=local_team,
                visitor_team=visitor_team,
                result=result,
            )
            self.content.controls.append(
                ft.Container(
                    content=ft.IconButton(
                        icon=ft.icons.EDIT,
                        icon_color=ft.colors.BLACK,
                        on_click=self._update_match_modal,
                    )
                )
            )

            self.delete_match = CalendarDeleteMatchModal(match_id=self.match_id)
            self.content.controls.append(
                ft.Container(
                    content=ft.IconButton(
                        icon=ft.icons.DELETE,
                        icon_color=ft.colors.BLACK,
                        on_click=self._delete_match_modal,
                    )
                )
            )

    def _update_match_modal(self, e: ft.ControlEvent):
        self.page.open(self.edit_match)

    def _delete_match_modal(self, e: ft.ControlEvent):
        self.page.open(self.delete_match)
