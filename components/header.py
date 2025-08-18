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


def test_toast(page: ft.Page):
    """토스트 테스트 함수"""
    show_toast(page, "토스트 테스트 메시지!", 3000)


def _create_search_area(page: ft.Page, page_width: int) -> ft.Container:
    """검색 영역 생성"""
    search_field = ft.TextField(
        hint_text="🔍 프롬프트 검색...",
        border=ft.InputBorder.OUTLINE,
        dense=True,
        width=min(300, page_width * 0.3),
        on_submit=lambda e: _perform_search(page, e.control.value)
    )
    
    # 검색 필드를 페이지 세션에 저장 (나중에 초기화용)
    page.session.set("search_field", search_field)
    
    search_button = ft.ElevatedButton(
        "검색",
        bgcolor=Colors.BLUE_400,
        color=Colors.WHITE,
        on_click=lambda e: _perform_search(page, search_field.value)
    )
    
    return ft.Container(
        content=ft.Row([search_field, search_button], tight=True),
        expand=True
    )


def _clear_search_results(page: ft.Page):
    """검색 결과 초기화"""
    try:
        if page.session.get("search_results") is not None:
            page.session.remove("search_results")
        if page.session.get("search_query") is not None:
            page.session.remove("search_query")
        if page.session.get("filter_category") is not None:
            page.session.remove("filter_category")
        if page.session.get("filter_ai_model") is not None:
            page.session.remove("filter_ai_model")
        
        # 검색 필드도 초기화
        search_field = page.session.get("search_field")
        if search_field:
            search_field.value = ""
            search_field.update()
        
        if page.route == "/":
            # 현재 메인 페이지에 있으면 뷰를 다시 빌드
            from app import build_home_view
            page.views[-1] = build_home_view(page)
            page.update()
        else:
            page.go("/")
    except Exception as e:
        print(f"[ERROR] 검색 결과 초기화 오류: {e}")


def _go_home_and_clear_filters(page: ft.Page):
    """홈으로 이동하고 모든 필터/검색 상태 초기화"""
    try:
        print("[DEBUG] 로고 클릭 - 홈으로 이동 및 필터 초기화")
        
        # 모든 검색/필터 상태 초기화
        if page.session.get("search_results") is not None:
            page.session.remove("search_results")
        if page.session.get("search_query") is not None:
            page.session.remove("search_query")
        if page.session.get("filter_category") is not None:
            page.session.remove("filter_category")
        if page.session.get("filter_ai_model") is not None:
            page.session.remove("filter_ai_model")
        
        # 검색 필드도 초기화
        search_field = page.session.get("search_field")
        if search_field:
            search_field.value = ""
            search_field.update()
        
        # 홈으로 강제 이동 및 새로고침
        if page.route == "/":
            # 현재 메인 페이지에 있으면 뷰를 다시 빌드
            from app import build_home_view
            page.views[-1] = build_home_view(page)
            page.update()
        else:
            page.go("/")
        
        show_toast(page, "홈으로 돌아갑니다.", 1000)
        
    except Exception as e:
        print(f"[ERROR] 홈 이동 오류: {e}")
        page.go("/")


def _perform_search(page: ft.Page, query: str):
    """검색 수행"""
    query = (query or "").strip()
    
    # 검색어가 없으면 전체 보기
    if not query:
        _clear_search_results(page)
        show_toast(page, "전체 프롬프트를 표시합니다.", 1000)
        return
    
    if len(query) < 2:
        show_toast(page, "검색어는 2자 이상 입력해주세요.", 1000)
        return
    
    try:
        # 검색 결과를 세션에 저장
        from services.search_service import search_prompts
        results = search_prompts(query)
        
        if not results:
            show_toast(page, f"'{query}' 검색 결과가 없습니다.", 1000)
            return
        
        # 검색 결과를 세션에 저장하고 메인 페이지로 이동
        page.session.set("search_query", query)
        page.session.set("search_results", results)
        
        show_toast(page, f"'{query}' 검색 결과 {len(results)}개 발견!", 1000)
        
        # 메인 페이지로 이동하고 강제로 새로고침
        if page.route != "/":
            page.go("/")
        else:
            # 현재 메인 페이지에 있으면 뷰를 다시 빌드
            from app import build_home_view
            page.views[-1] = build_home_view(page)
            page.update()
            
    except Exception as e:
        print(f"[ERROR] 검색 오류: {e}")
        show_toast(page, "검색 중 오류가 발생했습니다.", 1000)

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
            on_click=lambda e: _go_home_and_clear_filters(e.page),
        ),
        
        # 검색 영역 (반응형)
        _create_search_area(page, page_width),
        
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


