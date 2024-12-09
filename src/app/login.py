import flet as ft

from app.widgets.logo import Logo
from app.widgets.login_body import LoginBody
from app.register import Register
from app.widgets.snack_bar import SnackBar
from core.application.user.user_login_service import UserLoginService


class Login(LoginBody):
    def __init__(self):
        super().__init__()

    def build(self):
        self._build_function()

    def _build_function(self):
        self.user = ft.TextField(
            label=f"Usuario",
            border=ft.InputBorder.UNDERLINE,
            icon=ft.icons.PERSON,
            on_change=self._validate,
            autofill_hints=ft.AutofillHint.NAME,
        )
        self.password = ft.TextField(
            label="Contraseña",
            border=ft.InputBorder.UNDERLINE,
            icon=ft.icons.LOCK,
            password=True,
            can_reveal_password=True,
            on_change=self._validate,
            autofill_hints=ft.AutofillHint.PASSWORD,
        )

        self.save_login = ft.Checkbox(label="Recordar usuario")

        self.log_in_button = ft.ElevatedButton(
            text="Iniciar sesión",
            icon=ft.icons.LOGIN,
            on_click=self._log_in,
            disabled=True,
        )

        self.sign_in_button = ft.TextButton(text="Crear cuenta", on_click=self._sign_in)

        self.content = ft.AutofillGroup(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=Logo(size=30),
                        alignment=ft.alignment.center,
                        padding=ft.padding.only(bottom=20),
                    ),
                    ft.Container(
                        content=ft.Column(
                            controls=[self.user, self.password],
                        )
                    ),
                    ft.Container(
                        content=self.save_login,
                        padding=ft.padding.only(top=20, bottom=30),
                    ),
                    ft.Container(
                        content=self.log_in_button,
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Text("¿No tienes una cuenta?"),
                                self.sign_in_button,
                            ],
                        ),
                        padding=ft.padding.only(bottom=10),
                        alignment=ft.alignment.center,
                    ),
                ],
            ),
        )

    def _validate(self, event: ft.ControlEvent) -> None:
        if all([self.user.value, self.password.value]):
            self.log_in_button.disabled = False
        else:
            self.log_in_button.disabled = True

        self.update()
        self.page.update()

    def _log_in(self, event: ft.ControlEvent) -> None:
        user_login_service: UserLoginService = (
            self.page.container.services.user_login_service()
        )

        user = user_login_service(
            user_name=self.user.value, password=self.password.value
        )
        if user is not None:
            if self.save_login.value:
                self.page.save_token(user=user)

            self.page.clean()
            self.page.add(self.page.init_main_page(user=user))
            self.page.update()
        else:
            self.page.overlay.append(
                SnackBar(
                    text="Error al intentar inicar sesión. Usuario y/o contraseña desconocidos.",
                    success=False,
                    open=True,
                ),
            )
            self.page.update()

    def _sign_in(self, event: ft.ControlEvent) -> None:
        self.page.clean()

        self.page.add(Register())

        self.page.update()
