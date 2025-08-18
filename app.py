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


def _check_welcome_bonus(page: ft.Page):
    """환영 보너스 토스트 확인 및 표시"""
    try:
        bonus_points = page.session.get("welcome_bonus")
        if bonus_points:
            from components.toast import show_toast
            show_toast(page, f"🎉 회원가입 축하! 포인트 +{bonus_points}개 획득!", 3000)
            # 한 번 표시 후 세션에서 제거
            page.session.remove("welcome_bonus")
    except Exception as e:
        print(f"[DEBUG] 환영 보너스 토스트 오류: {e}")


def _update_ui_after_filter(page: ft.Page):
    """필터 적용 후 UI 직접 업데이트"""
    try:
        print("[DEBUG] UI 직접 업데이트 시작")
        
        # 1. 사이드바 업데이트 (필터 활성화 표시)
        # 2. 메인 카드 영역 업데이트 (필터링된 결과)
        
        # 현재 뷰에서 사이드바와 카드 컨테이너 찾기
        if not page.views:
            print("[ERROR] 페이지 뷰가 없음")
            page.go("/")
            return
            
        main_view = page.views[-1]
        
        # 뷰를 다시 빌드하는 것이 가장 확실함
        new_view = build_home_view(page)
        page.views[-1] = new_view
        page.update()
        
        print("[DEBUG] UI 직접 업데이트 완료")
        
    except Exception as e:
        print(f"[ERROR] UI 업데이트 실패: {e}")
        import traceback
        traceback.print_exc()
        # 폴백: 페이지 이동
        page.go("/")


def _create_filter_sidebar(page: ft.Page) -> ft.Container:
    """필터 사이드바 생성 - 간단 버전"""
    print("[DEBUG] _create_filter_sidebar 함수 시작")
    from components.toast import show_toast
    
    def apply_category_filter(category: str):
        """카테고리 필터 적용"""
        try:
            from services.csv_utils import read_csv_rows
            from pathlib import Path
            
            print(f"[DEBUG] 카테고리 필터 적용: {category}")
            
            # 기존 검색 결과만 초기화 (AI 모델 필터는 유지)
            if page.session.get("search_results") is not None:
                page.session.remove("search_results")
            if page.session.get("search_query") is not None:
                page.session.remove("search_query")
            # AI 모델 필터는 유지하여 중복 필터 가능
            
            if category == "전체":
                # 모든 필터 초기화 (전체 프롬프트 표시)
                if page.session.get("filter_category") is not None:
                    page.session.remove("filter_category")
                if page.session.get("filter_ai_model") is not None:
                    page.session.remove("filter_ai_model")
                if page.session.get("search_results") is not None:
                    page.session.remove("search_results")
                if page.session.get("search_query") is not None:
                    page.session.remove("search_query")
                
                show_toast(page, "전체 프롬프트를 표시합니다.", 1000)
                
                # 전체 선택 시 UI 업데이트
                print(f"[DEBUG] 전체 카테고리 선택 - 모든 필터 초기화 후 UI 업데이트")
                _update_ui_after_filter(page)
                return
            else:
                # 카테고리 필터 적용 (AI 모델 필터와 중복 적용)
                prompts_data = read_csv_rows(Path("data/prompts.csv"))
                filtered_results = []
                
                # 기존 AI 모델 필터 확인
                current_ai_model = page.session.get("filter_ai_model")
                
                for prompt in prompts_data:
                    prompt_category = prompt.get("category", "").strip()
                    prompt_ai_model = prompt.get("ai_model_key", "").strip()
                    
                    # 카테고리 조건 확인
                    category_match = (prompt_category == category)
                    
                    # AI 모델 조건 확인 (설정되어 있으면)
                    ai_model_match = True
                    if current_ai_model and current_ai_model != "전체":
                        ai_model_match = (prompt_ai_model == current_ai_model)
                    
                    # 두 조건 모두 만족하면 추가
                    if category_match and ai_model_match:
                        filtered_results.append(prompt)
                
                page.session.set("filter_category", category)
                page.session.set("search_results", filtered_results)
                print(f"[DEBUG] 세션 저장 완료 - filter_category: {category}, search_results: {len(filtered_results)}개")
                
                # 토스트 메시지에 중복 필터 정보 포함
                if current_ai_model and current_ai_model != "전체":
                    model_names = {"gpt4": "ChatGPT", "claude": "Claude", "gemini": "Gemini", "midjourney": "Midjourney"}
                    model_name = model_names.get(current_ai_model, current_ai_model)
                    show_toast(page, f"'{category}' + '{model_name}' 필터: {len(filtered_results)}개 프롬프트", 1000)
                else:
                    show_toast(page, f"'{category}' 카테고리 {len(filtered_results)}개 프롬프트", 1000)
            
            # 직접 UI 업데이트 (페이지 이동 없이)
            print(f"[DEBUG] 카테고리 필터 적용 후 직접 UI 업데이트: {category}")
            _update_ui_after_filter(page)
            
        except Exception as e:
            print(f"[ERROR] 카테고리 필터 오류: {e}")
            import traceback
            traceback.print_exc()
            show_toast(page, "필터 적용 중 오류가 발생했습니다.", 1000)
    
    def apply_ai_model_filter(ai_model_key: str):
        """AI 모델 필터 적용"""
        try:
            from services.csv_utils import read_csv_rows
            from pathlib import Path
            
            print(f"[DEBUG] AI 모델 필터 적용: {ai_model_key}")
            
            # 기존 검색 결과만 초기화 (카테고리 필터는 유지)
            if page.session.get("search_results") is not None:
                page.session.remove("search_results")
            if page.session.get("search_query") is not None:
                page.session.remove("search_query")
            # 카테고리 필터는 유지하여 중복 필터 가능
            
            if ai_model_key == "전체":
                # 모든 필터 초기화 (전체 프롬프트 표시)
                if page.session.get("filter_ai_model") is not None:
                    page.session.remove("filter_ai_model")
                if page.session.get("filter_category") is not None:
                    page.session.remove("filter_category")
                if page.session.get("search_results") is not None:
                    page.session.remove("search_results")
                if page.session.get("search_query") is not None:
                    page.session.remove("search_query")
                
                show_toast(page, "전체 프롬프트를 표시합니다.", 1000)
                
                # 전체 선택 시 UI 업데이트
                print(f"[DEBUG] 전체 AI 모델 선택 - 모든 필터 초기화 후 UI 업데이트")
                _update_ui_after_filter(page)
                return
            else:
                # AI 모델 필터 적용 (카테고리 필터와 중복 적용)
                prompts_data = read_csv_rows(Path("data/prompts.csv"))
                filtered_results = []
                
                # 기존 카테고리 필터 확인
                current_category = page.session.get("filter_category")
                
                for prompt in prompts_data:
                    prompt_category = prompt.get("category", "").strip()
                    prompt_ai_model = prompt.get("ai_model_key", "").strip()
                    
                    # AI 모델 조건 확인
                    ai_model_match = (prompt_ai_model == ai_model_key)
                    
                    # 카테고리 조건 확인 (설정되어 있으면)
                    category_match = True
                    if current_category and current_category != "전체":
                        category_match = (prompt_category == current_category)
                    
                    # 두 조건 모두 만족하면 추가
                    if ai_model_match and category_match:
                        filtered_results.append(prompt)
                
                # AI 모델 이름 매핑
                model_names = {
                    "gpt4": "ChatGPT",
                    "claude": "Claude", 
                    "gemini": "Gemini",
                    "midjourney": "Midjourney"
                }
                model_name = model_names.get(ai_model_key, ai_model_key)
                
                page.session.set("filter_ai_model", ai_model_key)
                page.session.set("search_results", filtered_results)
                print(f"[DEBUG] 세션 저장 완료 - filter_ai_model: {ai_model_key}, search_results: {len(filtered_results)}개")
                
                # 토스트 메시지에 중복 필터 정보 포함
                if current_category and current_category != "전체":
                    show_toast(page, f"'{current_category}' + '{model_name}' 필터: {len(filtered_results)}개 프롬프트", 1000)
                else:
                    show_toast(page, f"'{model_name}' 모델 {len(filtered_results)}개 프롬프트", 1000)
            
            # 직접 UI 업데이트 (페이지 이동 없이)
            print(f"[DEBUG] AI 모델 필터 적용 후 직접 UI 업데이트: {ai_model_key}")
            _update_ui_after_filter(page)
            
        except Exception as e:
            print(f"[ERROR] AI 모델 필터 오류: {e}")
            import traceback
            traceback.print_exc()
            show_toast(page, "필터 적용 중 오류가 발생했습니다.", 1000)
    
    # 실제 데이터에서 카테고리 목록 가져오기
    print("[DEBUG] 데이터 로딩 시작")
    try:
        from services.csv_utils import read_csv_rows
        from pathlib import Path
        
        prompts_data = read_csv_rows(Path("data/prompts.csv"))
        print(f"[DEBUG] 로딩된 프롬프트 개수: {len(prompts_data) if prompts_data else 0}")
        
        categories_set = set(["전체"])  # 전체는 기본 포함
        ai_models_set = set()
        
        for i, prompt in enumerate(prompts_data[:5]):  # 처음 5개만 디버그 출력
            print(f"[DEBUG] 프롬프트 {i+1}: category='{prompt.get('category', '')}', ai_model='{prompt.get('ai_model_key', '')}'")
        
        for prompt in prompts_data:
            # 카테고리 수집
            category = prompt.get("category", "").strip()
            if category and category not in ["", "1234"]:  # 빈 값이나 테스트 데이터 제외
                categories_set.add(category)
                print(f"[DEBUG] 카테고리 추가: '{category}'")
            
            # AI 모델 수집
            ai_model = prompt.get("ai_model_key", "").strip()
            if ai_model and ai_model not in ["", "1234"]:  # 빈 값이나 테스트 데이터 제외
                ai_models_set.add(ai_model)
                print(f"[DEBUG] AI 모델 추가: '{ai_model}'")
        
        # "전체"를 최상단으로, 나머지는 정렬
        categories_list = sorted([cat for cat in categories_set if cat != "전체"])
        categories = ["전체"] + categories_list
        print(f"[DEBUG] 실제 카테고리 목록: {categories}")
        
        # AI 모델 이름 매핑
        model_mapping = {
            "gpt4": "ChatGPT",
            "claude": "Claude",
            "gemini": "Gemini",
            "midjourney": "Midjourney",
            "stable_diffusion": "Stable Diffusion"
        }
        
        ai_models = [{"key": "전체", "name": "전체"}]
        for key in sorted(ai_models_set):
            name = model_mapping.get(key, key.title())
            ai_models.append({"key": key, "name": name})
        
        print(f"[DEBUG] 실제 AI 모델 목록: {ai_models}")
        
    except Exception as e:
        print(f"[ERROR] 데이터 로딩 오류: {e}")
        categories = ["전체", "텍스트"]
        ai_models = [{"key": "전체", "name": "전체"}, {"key": "gpt4", "name": "ChatGPT"}]
    
    # 카테고리 버튼들 생성
    current_category = page.session.get("filter_category") or ""
    print(f"[DEBUG] 사이드바 생성 시 현재 카테고리: '{current_category}'")
    category_buttons = []
    
    for category in categories:
        is_active = (category == current_category) or (category == "전체" and not current_category)
        print(f"[DEBUG] 카테고리 버튼 생성: {category}, 활성화: {is_active}, 현재 카테고리: {current_category}")
        
        button = ft.TextButton(
            text=f"{'▶ ' if is_active else '• '}{category}",
            style=ft.ButtonStyle(
                color=Colors.BLUE_600 if is_active else Colors.GREY_600,
                bgcolor=Colors.BLUE_50 if is_active else None,
            ),
            on_click=lambda e, cat=category: apply_category_filter(cat)
        )
        category_buttons.append(button)
    
    # AI 모델 버튼들 생성
    current_ai_model = page.session.get("filter_ai_model") or ""
    print(f"[DEBUG] 사이드바 생성 시 현재 AI 모델: '{current_ai_model}'")
    ai_model_buttons = []
    
    for model in ai_models:
        is_active = (model["key"] == current_ai_model) or (model["key"] == "전체" and not current_ai_model)
        print(f"[DEBUG] AI 모델 버튼 생성: {model['name']}, 활성화: {is_active}, 현재 모델: {current_ai_model}")
        
        button = ft.TextButton(
            text=f"{'▶ ' if is_active else '• '}{model['name']}",
            style=ft.ButtonStyle(
                color=Colors.BLUE_600 if is_active else Colors.GREY_600,
                bgcolor=Colors.BLUE_50 if is_active else None,
            ),
            on_click=lambda e, key=model["key"]: apply_ai_model_filter(key)
        )
        ai_model_buttons.append(button)
    
    return ft.Container(
        content=ft.Column([
            ft.Text("🔍 필터", size=16, weight=ft.FontWeight.BOLD),
            ft.Container(height=10),
            ft.Text("카테고리", size=14, weight=ft.FontWeight.BOLD),
            *category_buttons,
            ft.Container(height=10),
            ft.Text("AI 모델", size=14, weight=ft.FontWeight.BOLD),
            *ai_model_buttons,
        ]),
        width=UI_CONSTANTS["SIDEBAR_WIDTH"],
        padding=20,
        bgcolor=Colors.GREY_50,
    )


def build_home_view(page: ft.Page) -> ft.View:
    """홈 화면 - 반응형 레이아웃"""
    print("[DEBUG] build_home_view 시작")
    
    # 현재 세션 상태 확인
    current_category = page.session.get("filter_category")
    current_ai_model = page.session.get("filter_ai_model") 
    current_search_results = page.session.get("search_results")
    print(f"[DEBUG] 홈 뷰 생성 시 세션 상태 - 카테고리: {current_category}, AI모델: {current_ai_model}, 검색결과: {len(current_search_results) if current_search_results else 'None'}")
    
    try:
        header = create_header(page)
        print("[DEBUG] 헤더 생성 완료")
        
        # 현재 페이지 너비 확인
        page_width = getattr(page, 'window_width', 1200)
        print(f"[DEBUG] build_home_view 페이지 너비: {page_width}px")
        
        # 프롬프트 카드 컨테이너
        cards_container = ft.Column([], spacing=0, expand=True, scroll=ft.ScrollMode.AUTO)
        print("[DEBUG] 카드 컨테이너 생성 완료")
        
        # 반응형 래퍼 - prpt.ai 스타일
        def responsive_wrapper(main_content):
            
            if page_width >= 1000:
                # 큰 화면: 사이드바 + 메인 콘텐츠
                print("[DEBUG] 사이드바 생성 시작")
                filter_sidebar = _create_filter_sidebar(page)
                print("[DEBUG] 사이드바 생성 완료")
                
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
        print("[DEBUG] 반응형 래퍼 생성 완료")
        
        # View 생성
        home_view = ft.View(
            route="/",
            controls=[header, main_content],
            scroll=ft.ScrollMode.AUTO,
        )
        print("[DEBUG] View 생성 완료")
        
        # 카드 로딩 (이미 계산된 페이지 너비 사용)
        load_prompt_cards(cards_container, page, page_width)
        print("[DEBUG] 카드 로딩 완료")
        
        # 환영 보너스 토스트 체크
        _check_welcome_bonus(page)
        print("[DEBUG] 환영 보너스 체크 완료")
        
        return home_view
        
    except Exception as e:
        print(f"[ERROR] build_home_view 오류: {e}")
        import traceback
        traceback.print_exc()
        
        # 오류 발생 시 기본 뷰 반환
        return ft.View(
            route="/",
            controls=[
                ft.Container(
                    content=ft.Column([
                        ft.Text("홈 화면 로딩 중 오류가 발생했습니다.", size=16, color=Colors.RED),
                        ft.Text(f"오류: {e}", size=12, color=Colors.GREY_600),
                        ft.ElevatedButton("새로고침", on_click=lambda e: page.go("/"))
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=50,
                    alignment=ft.alignment.center
                )
            ],
            scroll=ft.ScrollMode.AUTO,
        )


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
    import os
    # 서버 배포용 설정 (Heroku, Railway 등)
    port = int(os.environ.get("PORT", 8000))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=port, host="0.0.0.0")