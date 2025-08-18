import flet as ft
from flet import Colors

from services.auth_service import authenticate_user
from components.header import create_header
from components.toast import show_toast


def _is_first_login(user_id: str) -> bool:
    """최초 로그인 여부 확인 (간단한 구현)"""
    try:
        from services.user_service import get_user_by_id
        user_data = get_user_by_id(user_id)
        if user_data:
            # 포인트가 초기값(100)이면 최초 로그인으로 간주
            points = int(user_data.get("points", 0))
            return points == 100
    except Exception:
        pass
    return False


def build_login_view(page: ft.Page) -> ft.View:
    header = create_header(page)
    username_field = ft.TextField(label="아이디", width=320)
    password_field = ft.TextField(label="비밀번호", width=320, password=True, can_reveal_password=True)

    def do_login(e):
        username = (username_field.value or "").strip()
        password = (password_field.value or "").strip()
        
        # 빈 필드 검증
        if not username:
            show_toast(page, "아이디를 입력해주세요.", 1000)
            return
        if not password:
            show_toast(page, "비밀번호를 입력해주세요.", 1000)
            return
        
        # 인증 시도
        res = authenticate_user(username, password)
        
        if not res.get("ok"):
            # 구체적인 에러 메시지 표시
            error_msg = res.get("msg", "로그인 실패")
            show_toast(page, error_msg, 1000)
            return
        
        # 로그인 성공
        page.session.set("user", res["user"])
        
        # 최초 로그인 체크 (회원가입 후 첫 로그인)
        user_data = res["user"]
        if _is_first_login(user_data.get("user_id")):
            # 축하 포인트 지급
            from services.points_service import add_points
            bonus_points = 50  # 회원가입 축하 포인트
            add_points(user_data.get("user_id"), bonus_points, "회원가입 축하")
            
            # 축하 토스트 (메인 페이지에서 표시하기 위해 세션에 저장)
            page.session.set("welcome_bonus", bonus_points)
        
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


