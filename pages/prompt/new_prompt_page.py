import time
import secrets
import flet as ft
from flet import Colors

from components.header import create_header
from services.prompt_service import save_new_prompt
from services.auth_service import get_current_user
from components.toast import show_toast

from config.constants import PLATFORM_OPTIONS, CATEGORY_OPTIONS


def _get_current_user(page: ft.Page):
    try:
        user = page.session.get("user")
        if isinstance(user, dict) and user.get("user_id"):
            return user
    except Exception:
        pass
    return None


def build_prompt_new_view(page: ft.Page) -> ft.View:
    header = create_header(page)
    current_user = _get_current_user(page)
    if not current_user:
        return ft.View(route="/prompt/new", controls=[header, ft.Container(content=ft.Text("로그인이 필요합니다."), padding=20)])

    title_field = ft.TextField(label="제목", width=480)
    content_field = ft.TextField(label="프롬프트 내용", width=480, multiline=True, min_lines=6)
    
    # 카테고리 드롭다운
    category_dropdown = ft.Dropdown(
        label="카테고리",
        value="텍스트",
        options=[ft.dropdown.Option(opt["key"], opt["label"]) for opt in CATEGORY_OPTIONS],
        width=240
    )
    
    # AI 모델 드롭다운
    ai_dropdown = ft.Dropdown(
        label="AI 모델",
        value="gpt4",
        options=[ft.dropdown.Option(opt["key"], opt["label"]) for opt in PLATFORM_OPTIONS],
        width=240
    )
    
    tags_field = ft.TextField(label="태그(쉼표 구분)", width=480)

    def save_prompt(e):
        # 현재 사용자 확인
        current_user = get_current_user(page)
        if not current_user:
            show_toast(page, "로그인이 필요합니다.", 2000)
            return
            
        # 입력 값 검증
        title = (title_field.value or "").strip()
        content = (content_field.value or "").strip()
        category = category_dropdown.value or "텍스트"
        ai_model = ai_dropdown.value or "gpt4"
        tags = (tags_field.value or "").strip()
        
        if not title:
            show_toast(page, "제목을 입력해주세요.", 2000)
            return
        if not content:
            show_toast(page, "프롬프트 내용을 입력해주세요.", 2000)
            return
        
        row = {
            "prompt_id": secrets.token_hex(12),
            "user_id": current_user["user_id"],
            "title": title,
            "content": content,
            "category": category,
            "ai_model_key": ai_model,
            "tags": tags,
            "likes": "0","bookmarks": "0","shares": "0","comments": "0","views": "0",
            "created_at": str(int(time.time())),
            "updated_at": str(int(time.time())),
        }
        save_new_prompt(row)
        
        # 프롬프트 작성 포인트 지급 (토스트 없이)
        from services.points_service import add_points
        if current_user:
            add_points(current_user.get("user_id"), 50, "프롬프트 작성")
        
        # 작성 완료 토스트 (포인트 정보 포함)
        show_toast(page, "프롬프트가 작성되었습니다. 포인트 +50개 획득!", 2000)
        # 홈으로 이동 후 목록을 강제 갱신
        try:
            page.go("/")
        except Exception:
            pass
        try:
            # 현재 뷰가 홈이면 재로딩 수행
            for ctrl in page.views[-1].controls:
                if isinstance(ctrl, ft.Container) and isinstance(ctrl.content, ft.Column):
                    from app import load_prompt_cards
                    load_prompt_cards(ctrl.content, page)
                    break
        except Exception:
            pass

    form = ft.Column([
        ft.Text("새 프롬프트 작성", size=20, weight=ft.FontWeight.BOLD),
        ft.Container(height=8),
        ft.Row([title_field]),
        content_field,
        ft.Row([category_dropdown, ai_dropdown], tight=True),
        tags_field,
        ft.Container(height=8),
        ft.ElevatedButton("등록", bgcolor=Colors.GREEN_400, color=Colors.WHITE, on_click=save_prompt),
    ])

    return ft.View(route="/prompt/new", controls=[header, ft.Container(content=form, padding=20)])


