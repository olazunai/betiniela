import flet as ft

from widgets.logo import Logo
from widgets.login_body import LoginBody
from register import Register
from navigation_bar import NavigationBar
from app_bar import AppBar


class Login(LoginBody):
    def __init__(self, page: ft.Page):
        super().__init__()

        self.page = page

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
            can_reveal_password=True,
            on_change=self._validate,
        )

        self.save_login = ft.Checkbox(label="Recordar usuario")

        self.log_in_button = ft.ElevatedButton(
            text="Iniciar sesión",
            icon=ft.icons.LOGIN,
            on_click=self._log_in,
            disabled=True,
        )

        self.sign_in_button = ft.TextButton(text="Crear cuenta", on_click=self._sign_in)

        self.content = ft.Column(
            controls=[
                ft.Container(
                    content=Logo(size=30),
                    alignment=ft.alignment.center,
                    padding=ft.padding.only(bottom=30),
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
                    padding=ft.padding.only(top=30, bottom=10),
                ),
            ],
        )

        self.logged = False

    async def _validate(self, event: ft.ControlEvent) -> None:
        if all([self.user.value, self.password.value]):
            self.log_in_button.disabled = False
        else:
            self.log_in_button.disabled = True

        self.page.update()

    async def _log_in(self, event: ft.ControlEvent) -> None:
        self.page.clean()

        self.page.appbar = AppBar(page=self.page)
        self.page.navigation_bar = NavigationBar(page=self.page)

        self.page.update()

    async def _sign_in(self, event: ft.ControlEvent) -> None:
        self.page.clean()

        self.page.add(Register(page=self.page))

        self.page.update()
