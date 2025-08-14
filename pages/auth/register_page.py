import flet as ft
from flet import Colors

from services.auth_service import register_user
from components.header import create_header
from components.toast import show_toast


def build_register_view(page: ft.Page) -> ft.View:
    header = create_header(page)
    username_field = ft.TextField(label="아이디", width=320)
    password_field = ft.TextField(label="비밀번호", width=320, password=True, can_reveal_password=True)

    def do_register(e):
        res = register_user(username_field.value or "", password_field.value or "")
        # 라우팅 후에도 보이도록 flash에 저장
        show_toast(page, res.get("msg", ""), 1000)
        # 실패 시 현재 페이지에서 즉시 표시 시도
        if not res.get("ok"):
            show_toast(page, res.get("msg", ""), 1000)
            return
        page.go("/login")

    body = ft.Column([
        ft.Text("회원가입", size=20, weight=ft.FontWeight.BOLD),
        ft.Container(height=8),
        username_field,
        password_field,
        ft.Container(height=8),
        ft.ElevatedButton("회원가입", bgcolor=Colors.GREEN_400, color=Colors.WHITE, on_click=do_register),
        ft.Container(height=8),
        ft.TextButton("로그인으로 돌아가기", on_click=lambda e: page.go("/login")),
    ])

    return ft.View(route="/register", controls=[header, ft.Container(content=body, padding=20)])


