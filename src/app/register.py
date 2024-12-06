import flet as ft

from app.main_page import MainPage
from core.application.user.user_creator_service import UserCreatorService
from app.widgets.login_body import LoginBody


class Register(LoginBody):
    def __init__(self):
        super().__init__()

    def build(self):
        return self._build_function()

    def _build_function(self):
        self.user = ft.TextField(
            label="Usuario",
            border=ft.InputBorder.UNDERLINE,
            icon=ft.icons.PERSON,
            on_change=self._validate,
        )
        self.password = ft.TextField(
            label="Contraseña",
            border=ft.InputBorder.UNDERLINE,
            icon=ft.icons.LOCK,
            password=True,
            on_change=self._validate,
        )
        self.confirm_password = ft.TextField(
            label="Confirmar contraseña",
            border=ft.InputBorder.UNDERLINE,
            password=True,
            on_change=self._validate,
        )

        self.sign_in_button = ft.ElevatedButton(
            text="Registrarse", on_click=self._sign_in, disabled=True
        )

        self.content = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            self.user,
                            self.password,
                            ft.Container(
                                content=self.confirm_password,
                                padding=ft.padding.only(left=40),
                            ),
                        ],
                    ),
                    padding=ft.padding.only(top=80),
                ),
                ft.Container(
                    content=self.sign_in_button,
                    alignment=ft.alignment.center,
                    padding=ft.padding.only(top=50),
                ),
            ],
        )
        return self.content

    def _validate(self, event: ft.ControlEvent) -> None:
        if all([self.user.value, self.password.value, self.confirm_password.value]):
            self.sign_in_button.disabled = False
        else:
            self.sign_in_button.disabled = True

        self.page.update()

    def _sign_in(self, event: ft.ControlEvent) -> None:
        user_creator_service: UserCreatorService = (
            self.page.container.services.user_creator_service()
        )

        user = user_creator_service(
            user_name=self.user.value,
            password=self.password.value,
        )

        self.page.clean()

        self.page.add(MainPage(user=user))

        self.page.update()
