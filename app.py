"""
Promptub 메인 애플리케이션 - 리팩토링된 버전
"""
import flet as ft
from flet import Colors

# 서비스 및 컴포넌트 import
from services.auth_service import get_current_user
from components.header import create_header
from components.prompt_card import load_prompt_cards
from pages.auth.login_page import build_login_view
from pages.auth.register_page import build_register_view  
from pages.prompt.new_prompt_page import build_prompt_new_view
from pages.prompt.detail_page import build_prompt_detail_view
from config.constants import UI_CONSTANTS


def build_home_view(page: ft.Page) -> ft.View:
    """홈 화면 - 반응형 레이아웃"""
    header = create_header(page)
    
    # 현재 페이지 너비 확인
    page_width = getattr(page, 'window_width', 1200)
    print(f"[DEBUG] build_home_view 페이지 너비: {page_width}px")
    
    # 프롬프트 카드 컨테이너
    cards_container = ft.Column([], spacing=0, expand=True, scroll=ft.ScrollMode.AUTO)
    
    # 반응형 래퍼 - prpt.ai 스타일
    def responsive_wrapper(main_content):
        
        if page_width >= 1000:
            # 큰 화면: 사이드바 + 메인 콘텐츠
            filter_sidebar = ft.Container(
                content=ft.Column([
                    ft.Text("🔍 필터", size=16, weight=ft.FontWeight.BOLD),
                    ft.Container(height=10),
                    ft.Text("카테고리", size=14, weight=ft.FontWeight.BOLD),
                    ft.Text("• 전체", size=12, color=Colors.GREY_600),
                    ft.Text("• 텍스트", size=12, color=Colors.GREY_600),
                    ft.Text("• 이미지", size=12, color=Colors.GREY_600),
                    ft.Container(height=10),
                    ft.Text("AI 모델", size=14, weight=ft.FontWeight.BOLD),
                    ft.Text("• ChatGPT", size=12, color=Colors.GREY_600),
                    ft.Text("• Claude", size=12, color=Colors.GREY_600),
                    ft.Text("• Midjourney", size=12, color=Colors.GREY_600),
                ]),
                width=UI_CONSTANTS["SIDEBAR_WIDTH"],
                padding=20,
                bgcolor=Colors.GREY_50,
            )
            
            content_wrapper = ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=filter_sidebar,
                        alignment=ft.alignment.top_left,  # 사이드바 상단 고정
                    ),
                    ft.Container(
                        content=main_content,
                        expand=True,
                        padding=ft.padding.only(left=20, right=20, top=20, bottom=20),
                    )
                ], 
                alignment=ft.MainAxisAlignment.START,  # Row 가로 정렬
                vertical_alignment=ft.CrossAxisAlignment.START),  # Row 세로 정렬 (상단 고정)
                width=min(UI_CONSTANTS["MAX_CONTENT_WIDTH"], page_width),
                alignment=ft.alignment.top_center,  # 전체 컨테이너도 상단 정렬
            )
        else:
            # 작은 화면: 메인 콘텐츠만
            content_wrapper = ft.Container(
                content=main_content,
                width=min(UI_CONSTANTS["MAX_CONTENT_WIDTH"], page_width),
                padding=20,
                alignment=ft.alignment.top_center,  # 상단 중앙 정렬
            )
        
        return ft.Container(
            content=content_wrapper,
            bgcolor=Colors.GREY_50,
            expand=True,
            alignment=ft.alignment.top_center,  # 상단 중앙 정렬
        )
    
    main_content = responsive_wrapper(cards_container)
    
    # View 생성
    home_view = ft.View(
        route="/",
        controls=[header, main_content],
        scroll=ft.ScrollMode.AUTO,
    )
    
    # 카드 로딩 (이미 계산된 페이지 너비 사용)
    load_prompt_cards(cards_container, page, page_width)
    
    return home_view


def main(page: ft.Page):
    """메인 애플리케이션 진입점"""
    # 기본 페이지 설정
    page.title = "Promptub - AI 프롬프트 공유 SNS"
    page.window_width = 1200
    page.window_height = 800
    page.window_resizable = True
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 0
    


    def on_resize(e):
        """페이지 크기 변경 시 홈 뷰 재구성"""
        try:
            if page.route == "/":
                new_width = getattr(page, 'window_width', 1200)
                print(f"[DEBUG] 페이지 리사이즈: {new_width}px")
                # 홈 뷰 재구성
                page.views[-1] = build_home_view(page)
                page.update()
        except Exception as ex:
            print(f"[DEBUG] 리사이즈 오류: {ex}")

    def route_change(e):
        """라우팅 처리"""
        # 로그아웃 직후 강제 새로고침 라우트 처리
        if (page.route or "/") == "/__refresh":
            page.go("/")
            return

        # 비로그인 상태에서 보호되지 않은 페이지만 허용하고 나머지는 메인으로 이동
        try:
            unauth_allowed = {"/", "/login", "/register"}
            current_user = page.session.get("user")
            is_authed = isinstance(current_user, dict) and current_user.get("user_id")
            if not is_authed and (page.route or "/") not in unauth_allowed:
                page.go("/")
                return
        except Exception:
            pass

        # 라우팅 처리
        page.views.clear()
        
        route = page.route or "/"
        print(f"[DEBUG] route_change: {route}")
        
        if route == "/":
            page.views.append(build_home_view(page))
        elif route == "/login":
            page.views.append(build_login_view(page))
        elif route == "/register":
            page.views.append(build_register_view(page))
        elif route == "/prompt/new":
            page.views.append(build_prompt_new_view(page))
        elif route.startswith("/prompt/") and len(route.split("/")) == 3:
            # /prompt/{id} 형태
            prompt_id = route.split("/")[-1]
            if prompt_id:
                page.views.append(build_prompt_detail_view(page, prompt_id))
            else:
                page.views.append(build_home_view(page))
        else:
            # 기본: 홈으로
            page.views.append(build_home_view(page))
        
        page.update()

    def view_pop(e):
        """뒤로가기 처리"""
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    # 이벤트 핸들러 등록
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.on_resize = on_resize  # 리사이즈 이벤트 등록
    
    # 초기 라우트 처리
    page.go(page.route or "/")


if __name__ == "__main__":
    # 웹 배포용 설정
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8000)