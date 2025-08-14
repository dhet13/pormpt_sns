"""
프롬프트 카드 UI 컴포넌트
"""
import flet as ft
from flet import Colors
from typing import Dict
import csv
from pathlib import Path
from config.constants import UI_CONSTANTS


def create_thumbnail_area(prompt_data: dict) -> ft.Container:
    """스마트 썸네일 시스템"""
    thumbnail_path = prompt_data.get("thumbnail_path", "")
    category = prompt_data.get("category", "텍스트")
    
    if thumbnail_path:
        # 1. 사용자가 업로드한 이미지 있으면 사용
        return create_user_image_thumbnail(thumbnail_path)
    else:
        # 2. 없으면 카테고리별 색상 + 이모지
        return create_category_thumbnail(category)


def create_user_image_thumbnail(thumbnail_path: str) -> ft.Container:
    """사용자 업로드 이미지 썸네일"""
    return ft.Container(
        content=ft.Image(src=thumbnail_path, fit=ft.ImageFit.COVER),
        width=60,
        height=60,
        border_radius=8,
        bgcolor=Colors.GREY_100,
    )


def create_category_thumbnail(category: str) -> ft.Container:
    """카테고리별 색상 + 이모지 썸네일"""
    category_config = {
        "텍스트": {"emoji": "📝", "color": Colors.BLUE_100},
        "이미지": {"emoji": "🎨", "color": Colors.PURPLE_100},
        "글쓰기": {"emoji": "✍️", "color": Colors.GREEN_100},
        "개발": {"emoji": "💻", "color": Colors.ORANGE_100},
        "마케팅": {"emoji": "📈", "color": Colors.RED_100},
        "교육": {"emoji": "📚", "color": Colors.INDIGO_100},
        "디자인": {"emoji": "🎨", "color": Colors.PINK_100},
        "업무": {"emoji": "💼", "color": Colors.BROWN_100},
    }
    
    config = category_config.get(category, {"emoji": "📝", "color": Colors.GREY_100})
    
    return ft.Container(
        content=ft.Text(config["emoji"], size=24),
        width=60,
        height=60,
        bgcolor=config["color"],
        border_radius=8,
        alignment=ft.alignment.center,
    )


def create_ai_badge(ai_model_key: str) -> ft.Container:
    """AI 모델 뱃지"""
    ai_config = {
        "gpt4": {"label": "ChatGPT", "color": Colors.GREEN_100, "text_color": Colors.GREEN_800},
        "claude": {"label": "Claude", "color": Colors.ORANGE_100, "text_color": Colors.ORANGE_800},
        "gemini": {"label": "Gemini", "color": Colors.BLUE_100, "text_color": Colors.BLUE_800},
        "midjourney": {"label": "MJ", "color": Colors.PURPLE_100, "text_color": Colors.PURPLE_800},
        "dalle": {"label": "DALL-E", "color": Colors.PINK_100, "text_color": Colors.PINK_800},
        "copilot": {"label": "Copilot", "color": Colors.INDIGO_100, "text_color": Colors.INDIGO_800},
        "stable_diffusion": {"label": "SD", "color": Colors.TEAL_100, "text_color": Colors.TEAL_800},
    }
    
    config = ai_config.get(ai_model_key, {"label": ai_model_key[:8], "color": Colors.GREY_100, "text_color": Colors.GREY_800})
    
    return ft.Container(
        content=ft.Text(config["label"], size=10, weight=ft.FontWeight.BOLD, color=config["text_color"]),
        bgcolor=config["color"],
        border_radius=12,
        padding=ft.padding.symmetric(horizontal=8, vertical=4),
    )


def create_category_badge(category: str) -> ft.Container:
    """카테고리 뱃지"""
    category_config = {
        "텍스트": {"color": Colors.BLUE_100, "text_color": Colors.BLUE_800},
        "이미지": {"color": Colors.PURPLE_100, "text_color": Colors.PURPLE_800},
        "글쓰기": {"color": Colors.GREEN_100, "text_color": Colors.GREEN_800},
        "개발": {"color": Colors.ORANGE_100, "text_color": Colors.ORANGE_800},
        "마케팅": {"color": Colors.RED_100, "text_color": Colors.RED_800},
        "교육": {"color": Colors.INDIGO_100, "text_color": Colors.INDIGO_800},
        "디자인": {"color": Colors.PINK_100, "text_color": Colors.PINK_800},
        "업무": {"color": Colors.BROWN_100, "text_color": Colors.BROWN_800},
    }
    
    config = category_config.get(category, {"color": Colors.GREY_100, "text_color": Colors.GREY_800})
    
    return ft.Container(
        content=ft.Text(category, size=10, weight=ft.FontWeight.BOLD, color=config["text_color"]),
        bgcolor=config["color"],
        border_radius=12,
        padding=ft.padding.symmetric(horizontal=8, vertical=4),
    )


def create_tags_row(tags_str: str) -> ft.Row:
    """태그 행 생성"""
    if not tags_str or not tags_str.strip():
        return ft.Row([])
    
    tags = [t.strip() for t in tags_str.split(",") if t.strip()]
    tag_controls = []
    
    for tag in tags[:3]:  # 최대 3개만 표시
        tag_controls.append(
            ft.Container(
                content=ft.Text(f"#{tag}", size=10, color=Colors.GREY_700),
                bgcolor=Colors.GREY_100,
                border_radius=8,
                padding=ft.padding.symmetric(horizontal=6, vertical=2),
            )
        )
    
    if len(tags) > 3:
        tag_controls.append(
            ft.Container(
                content=ft.Text(f"+{len(tags)-3}", size=10, color=Colors.GREY_600),
                bgcolor=Colors.GREY_50,
                border_radius=8,
                padding=ft.padding.symmetric(horizontal=6, vertical=2),
            )
        )
    
    return ft.Row(tag_controls, tight=True)


def create_prompt_card(prompt_data: dict, page: ft.Page, card_width: int = None) -> ft.Container:
    """마켓플레이스 스타일 프롬프트 카드"""
    from services.auth_service import get_current_user
    from services.interactions_service import toggle_like, toggle_bookmark, record_view, record_share
    from services.prompt_service import increment_prompt_stat
    
    # 카드 너비 설정 (동적 또는 기본값)
    if card_width is None:
        card_width = UI_CONSTANTS["CARD_WIDTH"]
    
    # 식별자 및 통계 텍스트 컨트롤
    prompt_id = str(prompt_data.get("prompt_id") or prompt_data.get("id") or "")
    # 안전한 prompt_id 확보 (아래 on_tap 람다에서 사용되므로 먼저 계산)
    safe_prompt_id = prompt_id or str(prompt_data.get("prompt_id") or prompt_data.get("id") or "")
    likes_text = ft.Text(str(prompt_data.get("likes", "0")), size=11, color=Colors.GREY_600)
    shares_text = ft.Text(str(prompt_data.get("shares", "0")), size=11, color=Colors.GREY_600)
    comments_text = ft.Text(str(prompt_data.get("comments", "0")), size=11, color=Colors.GREY_600)
    bookmarks_text = ft.Text(str(prompt_data.get("bookmarks", "0")), size=11, color=Colors.GREY_600)
    views_text = ft.Text(str(prompt_data.get("views", "0")), size=11, color=Colors.GREY_600)

    def _handle_stat(field: str, label_text: ft.Text, delta: int = 1):
        try:
            new_val = increment_prompt_stat(prompt_id, field, delta)
            if new_val is None:
                from services.csv_utils import safe_int
                new_val = safe_int(label_text.value, 0) + delta
            label_text.value = str(max(0, new_val))
            label_text.update()
        except Exception as ex:
            print(f"stat update error({field}): {ex}")

    current_user = get_current_user(page)
    current_user_id = current_user.get("user_id") if current_user else ""

    def on_like_click(e):
        try:
            liked, total = toggle_like(current_user_id or "guest", prompt_id)
            likes_text.value = str(total)
            likes_text.update()
        except Exception as ex:
            print(f"like toggle error: {ex}")

    def on_share_click(e):
        try:
            total = record_share(current_user_id, prompt_id)
            shares_text.value = str(total)
            shares_text.update()
        except Exception as ex:
            print(f"share record error: {ex}")

    def on_bookmark_click(e):
        try:
            marked, total = toggle_bookmark(current_user_id or "guest", prompt_id)
            bookmarks_text.value = str(total)
            bookmarks_text.update()
        except Exception as ex:
            print(f"bookmark toggle error: {ex}")

    def on_card_click(e):
        # 비회원은 상세보기 차단 → 가입/로그인 유도 모달
        if not current_user_id:
            from components.toast import show_toast
            show_toast(page, "로그인이 필요합니다.", 1000)
            return

        # 포인트 차감(라이트) 적용 (회원만)
        try:
            from services.points_service import try_consume_view
            res = try_consume_view(current_user_id)
            if not res.get("ok"):
                dlg = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("포인트 부족"),
                    content=ft.Text("이 프롬프트를 보려면 포인트가 부족합니다. 일일 무료 조회가 소진되었습니다."),
                    actions=[
                        ft.TextButton("닫기", on_click=lambda ev: (setattr(dlg, "open", False), page.update())),
                        ft.TextButton("로그인/충전", on_click=lambda ev: (setattr(dlg, "open", False), page.go("/login"))),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )
                page.dialog = dlg
                dlg.open = True
                page.update()
                return

            # 상세 페이지 진입 시 조회수 업데이트
            total = record_view(current_user_id, prompt_id)
            views_text.value = str(total)
            try:
                views_text.update()
            except Exception:
                pass
        except Exception as ex:
            print(f"view record error: {ex}")
        
        print(f"[DEBUG] navigate detail id: {safe_prompt_id}")  # Debug print
        page.go(f"/prompt/{safe_prompt_id}")

    def on_hover(e):
        try:
            if e.data == "true":
                e.control.bgcolor = Colors.BLUE_50
                e.control.shadow = [ft.BoxShadow(
                    spread_radius=2,
                    blur_radius=12,
                    color=Colors.with_opacity(0.15, Colors.BLUE_400),
                    offset=ft.Offset(0, 4)
                )]
                e.control.border = ft.border.all(2, Colors.BLUE_200)
                e.control.scale = 1.02
            else:
                e.control.bgcolor = Colors.WHITE
                e.control.shadow = [ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=4,
                    color=Colors.with_opacity(0.1, Colors.BLACK),
                    offset=ft.Offset(0, 2)
                )]
                e.control.border = ft.border.all(1, Colors.GREY_300)
                e.control.scale = 1.0
            e.control.update()
        except Exception:
            pass
    
    # 통계 버튼들 (이벤트 전파 방지)
    def stop_propagation_and_execute(func):
        def wrapper(e):
            try:
                func(e)
                # 이벤트 전파 중단
                if hasattr(e, 'control'):
                    e.control.data = "stats_clicked"
            except Exception as ex:
                print(f"stats click error: {ex}")
        return wrapper
    
    like_cluster = ft.Container(
        content=ft.Row([ft.Text("❤️", size=10), likes_text], spacing=2, tight=True),
        on_click=stop_propagation_and_execute(on_like_click),
        padding=ft.padding.symmetric(horizontal=3, vertical=2),
        border_radius=4,
    )
    share_cluster = ft.Container(
        content=ft.Row([ft.Text("📤", size=10), shares_text], spacing=2, tight=True),
        on_click=stop_propagation_and_execute(on_share_click),
        padding=ft.padding.symmetric(horizontal=3, vertical=2),
        border_radius=4,
    )
    comment_cluster = ft.Container(
        content=ft.Row([ft.Text("💬", size=10), comments_text], spacing=2, tight=True),
        padding=ft.padding.symmetric(horizontal=3, vertical=2),
        border_radius=4,
    )
    bookmark_cluster = ft.Container(
        content=ft.Row([ft.Text("🔖", size=10), bookmarks_text], spacing=2, tight=True),
        on_click=stop_propagation_and_execute(on_bookmark_click),
        padding=ft.padding.symmetric(horizontal=3, vertical=2),
        border_radius=4,
    )
    views_cluster = ft.Container(
        content=ft.Row([ft.Text("👁️", size=10), views_text], spacing=2, tight=True),  # 아이콘 크기 축소, 간격 축소
        padding=ft.padding.symmetric(horizontal=3, vertical=2),  # 패딩 축소
        border_radius=4,
    )

    # 썸네일과 제목 영역도 상세보기 클릭 가능하게 래핑
    is_authed = bool(current_user_id)
    def soft_block_login(e):
        try:
            from components.toast import show_toast
            show_toast(page, "로그인이 필요합니다.", 1000)
        except Exception:
            try:
                page.snack_bar = ft.SnackBar(ft.Text("로그인이 필요합니다."), open=True, duration=1000)
                page.update()
            except Exception:
                pass


    # 상단: 썸네일 + 제목 + 뱃지들 (클릭 이벤트 제거)
    header_row = ft.Row([
        create_thumbnail_area(prompt_data),
        ft.Container(width=12),
        ft.Column([
            ft.Text(
                prompt_data.get("title", "제목 없음")[:30] + ("..." if len(prompt_data.get("title", "")) > 30 else ""),
                size=14,
                weight=ft.FontWeight.BOLD,
                color=Colors.BLACK87,
            ),
            ft.Container(height=4),
            ft.Row([
                create_ai_badge(prompt_data.get("ai_model_key", "gpt4")),
                ft.Container(width=6),
                create_category_badge(prompt_data.get("category", "텍스트")),
            ], tight=True),
        ], expand=True),
    ], tight=True)
    
    # 하단: 통계 묶음 (조회수 노출을 위해 간격 축소)
    stats_row = ft.Row([
        like_cluster,
        ft.Container(width=8),  # 간격 축소: 12→8
        share_cluster,
        ft.Container(width=8),  # 간격 축소: 12→8
        comment_cluster,
        ft.Container(width=8),  # 간격 축소: 12→8
        bookmark_cluster,
        ft.Container(width=8),  # 간격 축소: 12→8
        views_cluster,  # expand 제거하여 조회수 확실히 노출
    ], tight=True)
    
    # 카드 전체 클릭 이벤트 (통계 버튼 제외)
    def on_card_click(e):
        # 통계 버튼 클릭인지 확인
        if hasattr(e, 'control') and getattr(e.control, 'data', None) == "stats_clicked":
            return  # 통계 버튼 클릭이면 상세페이지로 이동하지 않음
            
        if not is_authed:
            soft_block_login(e)
            return

        # 상세 페이지 진입 시 조회수 업데이트
        from services.interactions_service import record_view
        total = record_view(current_user_id, safe_prompt_id)
        
        print(f"[DEBUG] navigate detail id: {safe_prompt_id}")  # Debug print
        page.go(f"/prompt/{safe_prompt_id}")

    return ft.Container(
        content=ft.Column([
            header_row,
            ft.Container(height=8),
            ft.Text(
                prompt_data.get("content", "내용이 없습니다.")[:80] + ("..." if len(prompt_data.get("content", "")) > 80 else ""),
                size=12,
                color=Colors.GREY_700,
            ),
            ft.Container(height=8),
            create_tags_row(prompt_data.get("tags", "")),
            ft.Container(height=8),
            stats_row,
        ], tight=True),
        width=card_width,
        padding=12,
        margin=6,
        bgcolor=Colors.WHITE,
        border_radius=12,
        border=ft.border.all(1, Colors.GREY_300),
        shadow=[ft.BoxShadow(
            spread_radius=0,
            blur_radius=4,
            color=Colors.with_opacity(0.1, Colors.BLACK),
            offset=ft.Offset(0, 2)
        )],
        animate=200,
        animate_scale=200,
        on_hover=on_hover,
        on_click=on_card_click,  # 카드 전체 클릭 이벤트 추가
    )


def load_prompt_cards(container: ft.Column, page: ft.Page, page_width: int = None):
    """프롬프트 카드 로딩 및 그리드 배치"""
    from services.csv_utils import read_csv_rows
    
    try:
        # CSV에서 프롬프트 데이터 로드
        prompts_data = read_csv_rows(Path("data/prompts.csv"))
        
        if not prompts_data:
            container.controls = [ft.Text("프롬프트가 없습니다.", size=16, color=Colors.GREY_600)]
            return
        
        # 최신순 정렬 (빈 문자열 처리)
        def safe_sort_key(x):
            created_at = x.get("created_at", "0")
            if not created_at or created_at.strip() == "":
                return 0
            try:
                return int(created_at)
            except ValueError:
                return 0
        
        prompts_data.sort(key=safe_sort_key, reverse=True)
        
        # 간단한 반응형 카드 너비 계산
        def get_responsive_card_width(page_width: int):
            """화면 크기에 따른 카드 너비 계산"""
            # 사이드바 너비 계산
            sidebar_width = UI_CONSTANTS["SIDEBAR_WIDTH"] if page_width >= 1000 else 0
            content_padding = 40
            available_width = page_width - sidebar_width - content_padding
            
            print(f"[DEBUG] 반응형 계산: page_width={page_width}, sidebar_width={sidebar_width}, available_width={available_width}")
            
            # 3개 배치를 위한 더 관대한 조건
            if available_width >= 800:  # 3개 배치 (더 완화: 900→800)
                card_width = (available_width - 24) // 3  # 간격 제외하고 3등분
                print(f"[DEBUG] 3개 배치 선택: {card_width}px")
            elif available_width >= 550:  # 2개 배치 (더 완화: 600→550)
                card_width = (available_width - 12) // 2  # 간격 제외하고 2등분
                print(f"[DEBUG] 2개 배치 선택: {card_width}px")
            else:  # 1개 배치
                card_width = min(available_width - 20, 400)  # 최대 400px
                print(f"[DEBUG] 1개 배치 선택: {card_width}px")
            
            # 최소/최대 너비 제한 (최대 300px로 제한)
            card_width = max(250, min(card_width, 600))
            
            print(f"[DEBUG] 최종 카드 너비: {card_width}px (available_width: {available_width}px)")
            return card_width
        
        # 페이지 너비에 따른 반응형 카드 너비 계산
        if page_width is None:
            page_width = getattr(page, 'window_width', 1200)
        
        dynamic_card_width = get_responsive_card_width(page_width)
        
        # 카드들을 생성 (동적 너비 적용)
        cards = []
        for prompt in prompts_data:
            card = create_prompt_card(prompt, page, dynamic_card_width)
            cards.append(card)
        
        # prpt.ai 스타일: wrap=True로 자동 반응형 배치
        if cards:
            cards_row = ft.Row(
                controls=cards,
                spacing=UI_CONSTANTS["GRID_SPACING"],
                alignment=ft.MainAxisAlignment.START,
                wrap=True,  # 자동 줄바꿈으로 반응형 구현
                run_spacing=10,  # 행 간격
            )
            container.controls = [cards_row]
        else:
            container.controls = [
                ft.Container(
                    content=ft.Text("프롬프트가 없습니다.", size=16, color=Colors.GREY_500),
                    alignment=ft.alignment.center,
                    height=200,
                )
            ]
        
    except Exception as ex:
        print(f"[ERROR] load_prompt_cards: {ex}")
        container.controls = [ft.Text(f"카드 로딩 오류: {ex}", color=Colors.RED)]
