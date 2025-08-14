import flet as ft
from flet import Colors

from services.auth_service import authenticate_user
from components.header import create_header
from components.toast import show_toast


def build_login_view(page: ft.Page) -> ft.View:
    header = create_header(page)
    username_field = ft.TextField(label="아이디", width=320)
    password_field = ft.TextField(label="비밀번호", width=320, password=True, can_reveal_password=True)

    def do_login(e):
        res = authenticate_user(username_field.value or "", password_field.value or "")
        # 라우팅 이후에도 표시되도록 flash에 저장
        show_toast(page, res.get("msg", "로그인 시도"), 1000)
        if not res.get("ok"):
            # 실패 시 현재 페이지에서 즉시 스낵 표시도 시도
            show_toast(page, res.get("msg", "로그인 실패"), 1000)
            return
        page.session.set("user", res["user"]) 
        page.go("/")

    register_hint = ft.Row([
        ft.Text("아직 계정이 없으신가요?"),
        ft.TextButton("회원가입", on_click=lambda e: page.go("/register")),
    ], tight=True)

    body = ft.Column([
        ft.Text("로그인", size=20, weight=ft.FontWeight.BOLD),
        ft.Container(height=8),
        username_field,
        password_field,
        ft.Container(height=8),
        ft.ElevatedButton("로그인", bgcolor=Colors.BLUE_400, color=Colors.WHITE, on_click=do_login),
        ft.Container(height=8),
        register_hint,
    ])

    return ft.View(route="/login", controls=[header, ft.Container(content=body, padding=20)])


