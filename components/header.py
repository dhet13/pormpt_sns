import flet as ft
from flet import Colors
from components.toast import show_toast


def _get_current_user(page: ft.Page):
    try:
        user = page.session.get("user")
        if isinstance(user, dict) and user.get("user_id"):
            return user
    except Exception:
        pass
    return None


def build_user_menu(page: ft.Page) -> ft.Row:
    current_user = _get_current_user(page)
    from services.user_service import get_user_by_id
    from services.points_service import _count_views_today
    from config.constants import FREE_VIEWS_PER_DAY

    def go_new_prompt(e):
        if not _get_current_user(page):
            page.snack_bar = ft.SnackBar(ft.Text("로그인이 필요합니다."))
            page.snack_bar.open = True
            page.go("/login")
            return
        page.go("/prompt/new")

    if current_user:
        # 포인트/무료 조회 잔여 계산
        user_row = get_user_by_id(current_user.get('user_id')) or {}
        try:
            points_val = int(user_row.get('points') or 0)
        except Exception:
            points_val = 0
        used_today = _count_views_today(current_user.get('user_id'))
        free_left = max(0, FREE_VIEWS_PER_DAY - used_today)

        def do_logout(e):
            # 세션 클리어
            try:
                try:
                    page.session.remove("user")
                except Exception:
                    pass
                page.session.set("user", None)
                page.session.clear()
            except Exception:
                pass
            # 메인으로 강제 이동: 뷰를 직접 재구성
            try:
                page.views.clear()
                from app import build_home_view
                page.views.append(build_home_view(page))
            except Exception:
                # 폴백: 라우팅 시도
                try:
                    page.go("/")
                except Exception:
                    pass
            page.update()
        return ft.Row([
            ft.Text(f"안녕, {current_user.get('username')}", size=12, color=Colors.GREY_700),
            ft.Container(width=8),
            ft.Container(
                content=ft.Row([
                    ft.Text("💰", size=12), ft.Text(str(points_val), size=12)
                ], tight=True),
                bgcolor=Colors.GREEN_50,
                border=ft.border.all(1, Colors.GREEN_200),
                border_radius=8,
                padding=6,
            ),
            ft.Container(width=6),
            ft.Container(
                content=ft.Row([
                    ft.Text("🎁", size=12), ft.Text(f"{free_left}/{FREE_VIEWS_PER_DAY}", size=12)
                ], tight=True),
                bgcolor=Colors.BLUE_50,
                border=ft.border.all(1, Colors.BLUE_200),
                border_radius=8,
                padding=6,
            ),
            ft.ElevatedButton(
                "✏️ 새 프롬프트",
                bgcolor=Colors.GREEN_400,
                color=Colors.WHITE,
                on_click=go_new_prompt,
            ),
            ft.ElevatedButton(
                "로그아웃",
                bgcolor=Colors.GREY_600,
                color=Colors.WHITE,
                on_click=do_logout
            ),
        ])
    else:
        return ft.Row([
            ft.ElevatedButton(
                "👤 로그인",
                bgcolor=Colors.GREY_600,
                color=Colors.WHITE,
                on_click=lambda e: page.go("/login")
            ),
        ])


def create_header(page: ft.Page) -> ft.Container:
    # 현재 페이지 너비 (기본값 1200)
    page_width = getattr(page, 'width', 1200) or 1200
    
    # 반응형 헤더 내용
    header_content = ft.Row([
        # 로고 영역
        ft.Container(
            content=ft.Row([
                ft.Text("🚀", size=28),
                ft.Text("Promptub", size=24, weight=ft.FontWeight.BOLD, color=Colors.BLUE_700)
            ], tight=True),
            on_click=lambda e: e.page.go("/"),
        ),
        
        # 검색 영역 (반응형)
        ft.Container(
            content=ft.Row([
                ft.TextField(
                    hint_text="🔍 프롬프트 검색...",
                    border=ft.InputBorder.OUTLINE,
                    dense=True,
                    width=min(300, page_width * 0.3)  # 화면 크기에 따라 조정
                ),
                ft.ElevatedButton(
                    "검색",
                    bgcolor=Colors.BLUE_400,
                    color=Colors.WHITE
                )
            ], tight=True),
            expand=True
        ),
        
        # 사용자 메뉴
        build_user_menu(page)
    ])
    
    # 큰 화면에서 중앙 정렬을 위한 래퍼
    if page_width >= 1200:
        header_wrapper = ft.Container(
            content=ft.Container(
                content=header_content,
                width=min(page_width, 1400),  # 최대 너비 제한
                alignment=ft.alignment.center
            ),
            alignment=ft.alignment.center
        )
    else:
        header_wrapper = header_content
    
    return ft.Container(
        content=header_wrapper,
        bgcolor=Colors.WHITE,
        padding=20,
        border=ft.border.only(bottom=ft.BorderSide(2, Colors.GREY_200)),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=4,
            color=Colors.with_opacity(0.1, Colors.BLACK),
            offset=ft.Offset(0, 2)
        )
    )


