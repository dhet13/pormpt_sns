"""
Promptub 간단 테스트 버전
"""
import flet as ft
from flet import Colors

# 서비스 및 컴포넌트 import
from components.header import create_header
from components.prompt_card.card_main import load_prompt_cards
from pages.auth.login_page import build_login_view
from pages.auth.register_page import build_register_view  
from pages.prompt.new_prompt_page import build_prompt_new_view
from pages.prompt.detail_page import build_prompt_detail_view


def _check_welcome_bonus(page: ft.Page):
    """환영 보너스 토스트 확인 및 표시"""
    try:
        bonus_points = page.session.get("welcome_bonus")
        if bonus_points:
            from components.toast import show_toast
            show_toast(page, f"🎉 회원가입 축하! 포인트 +{bonus_points}개 획득!", 3000)
            page.session.remove("welcome_bonus")
    except Exception as e:
        print(f"[DEBUG] 환영 보너스 토스트 오류: {e}")


def build_home_view(page: ft.Page) -> ft.View:
    """홈 화면 - 간단 버전"""
    print("[DEBUG] build_home_view 시작")
    
    try:
        header = create_header(page)
        print("[DEBUG] 헤더 생성 완료")
        
        # 프롬프트 카드 컨테이너
        cards_container = ft.Column([], spacing=10, expand=True, scroll=ft.ScrollMode.AUTO)
        print("[DEBUG] 카드 컨테이너 생성 완료")
        
        # 메인 콘텐츠
        main_content = ft.Container(
            content=cards_container,
            padding=20,
            expand=True,
        )
        print("[DEBUG] 메인 콘텐츠 생성 완료")
        
        # View 생성
        home_view = ft.View(
            route="/",
            controls=[header, main_content],
            scroll=ft.ScrollMode.AUTO,
        )
        print("[DEBUG] View 생성 완료")
        
        # 카드 로딩
        load_prompt_cards(cards_container, page)
        print("[DEBUG] 카드 로딩 완료")
        
        # 환영 보너스 확인
        _check_welcome_bonus(page)
        print("[DEBUG] 환영 보너스 확인 완료")
        
        return home_view
        
    except Exception as e:
        print(f"[ERROR] build_home_view 오류: {e}")
        import traceback
        traceback.print_exc()
        
        # 오류 발생 시 기본 뷰 반환
        return ft.View(
            route="/",
            controls=[
                ft.Text("홈 화면 로딩 중 오류가 발생했습니다.", size=16, color=Colors.RED),
                ft.Text(f"오류: {e}", size=12, color=Colors.GREY_600)
            ],
            scroll=ft.ScrollMode.AUTO,
        )


def main(page: ft.Page):
    """메인 함수"""
    print("[DEBUG] main 함수 시작")
    
    # 페이지 설정
    page.title = "Promptub"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.spacing = 0
    
    # 창 크기 설정
    page.window_width = 1200
    page.window_height = 800
    page.window_min_width = 400
    page.window_min_height = 600
    
    print("[DEBUG] 페이지 설정 완료")

    def on_resize(e):
        """창 크기 변경 시 처리"""
        try:
            if hasattr(page, 'window_width') and hasattr(page, 'window_height'):
                print(f"[DEBUG] 창 크기 변경: {page.window_width}x{page.window_height}")
                page.update()
        except Exception as ex:
            print(f"[DEBUG] 리사이즈 오류: {ex}")

    def route_change(e):
        """라우팅 처리"""
        print(f"[DEBUG] route_change: {page.route}")
        
        try:
            page.views.clear()
            
            route = page.route or "/"
            
            if route == "/":
                page.views.append(build_home_view(page))
            elif route == "/login":
                page.views.append(build_login_view(page))
            elif route == "/register":
                page.views.append(build_register_view(page))
            elif route == "/prompt/new":
                page.views.append(build_prompt_new_view(page))
            elif route.startswith("/prompt/") and len(route.split("/")) == 3:
                prompt_id = route.split("/")[-1]
                if prompt_id:
                    page.views.append(build_prompt_detail_view(page, prompt_id))
                else:
                    page.views.append(build_home_view(page))
            else:
                page.views.append(build_home_view(page))
            
            page.update()
            print(f"[DEBUG] 라우팅 완료: {route}")
            
        except Exception as ex:
            print(f"[ERROR] 라우팅 오류: {ex}")
            import traceback
            traceback.print_exc()

    def view_pop(e):
        """뒤로가기 처리"""
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    # 이벤트 핸들러 등록
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.on_resize = on_resize
    
    print("[DEBUG] 이벤트 핸들러 등록 완료")
    
    # 초기 라우트 처리
    page.go(page.route or "/")
    print("[DEBUG] 초기 라우트 처리 완료")


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8001))  # 다른 포트 사용
    print(f"[DEBUG] 서버 시작: http://localhost:{port}")
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=port, host="0.0.0.0")
