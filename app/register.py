import flet as ft

from app.widgets.snack_bar import SnackBar
from src.core.domain.exceptions import UserAlreadyExistsException
from src.core.application.user.user_creator_service import UserCreatorService
from app.widgets.login_body import LoginBody


class Register(LoginBody):
    def __init__(self):
        super().__init__()

    def build(self):
        self._build_function()

    def _build_function(self):
        self.user = ft.TextField(
            label="Usuario",
            border=ft.InputBorder.UNDERLINE,
            icon=ft.Icons.PERSON,
            on_change=self._validate,
        )
        self.password = ft.TextField(
            label="Contraseña",
            border=ft.InputBorder.UNDERLINE,
            icon=ft.Icons.LOCK,
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
                    content=ft.IconButton(
                        icon=ft.Icons.ARROW_BACK, on_click=self._go_login
                    ),
                ),
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
                    padding=ft.padding.only(top=60),
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
        if self.password.value != self.confirm_password.value:
            self.page.overlay.append(
                SnackBar(
                    text="Las contraseñas deben ser iguales. Intentelo de nuevo.",
                    success=False,
                    open=True,
                ),
            )
            self.page.update()
            return

        user_creator_service: UserCreatorService = (
            self.page.container.services.user_creator_service
        )

        try:
            user = user_creator_service(
                user_name=self.user.value,
                password=self.password.value,
            )

            self.page.clean()
            self.page.add(self.page.init_main_page(user=user))
            self.page.update()

        except UserAlreadyExistsException:
            self.page.overlay.append(
                SnackBar(
                    text=f"Este nombre de usuario ya existe.",
                    success=False,
                    open=True,
                ),
            )
            self.page.update()

        except Exception as e:
            self.page.overlay.append(
                SnackBar(
                    text=f"Error al intentar registrarse. {e}.",
                    success=False,
                    open=True,
                ),
            )
            self.page.update()

    def _go_login(self, e: ft.ControlEvent):
        self.page.logout(e)
