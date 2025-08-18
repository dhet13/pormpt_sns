"""
메인 프롬프트 카드 컴포넌트
"""
import flet as ft
from flet import Colors
from typing import Dict, Any, Optional
from pathlib import Path

from config.app_config import config
from ..common_handlers import create_navigation_handler, create_hover_handler
from utils.error_handler import safe_execute, ErrorType, handle_error
from .card_thumbnails import create_thumbnail_area
from .card_badges import create_ai_badge, create_category_badge, create_tags_row
from .card_stats import create_stats_controls, create_stats_row


def create_prompt_card(
    prompt_data: Dict[str, Any], 
    page: ft.Page, 
    card_width: Optional[int] = None
) -> ft.Container:
    """리팩토링된 프롬프트 카드 생성"""
    
    # 카드 너비 설정
    if card_width is None:
        page_width = getattr(page, 'window_width', 1200)
        card_width = config.get_responsive_card_width(page_width)
    
    # 현재 사용자 정보
    current_user_id = _get_current_user_id(page)
    prompt_id = str(prompt_data.get("prompt_id") or prompt_data.get("id") or "")
    
    # 카드 구성 요소들 생성
    header_row = _create_header_row(prompt_data)
    content_text = _create_content_text(prompt_data)
    tags_row = create_tags_row(prompt_data.get("tags", ""))
    
    # 통계 컨트롤들 생성
    stats_controls = create_stats_controls(prompt_data, current_user_id, page)
    stats_row = create_stats_row(stats_controls)
    
    # 카드 클릭 핸들러
    card_click_handler = create_navigation_handler(
        page=page,
        route=f"/prompt/{prompt_id}",
        auth_required=True,
        point_cost=config.business.POINT_COST_PER_VIEW,
        error_msg="프롬프트 상세보기 중 오류가 발생했습니다."
    )
    
    # 호버 핸들러
    hover_handler = create_hover_handler(
        hover_style=_convert_hover_style(config.ui.CARD_HOVER_STYLE),
        normal_style=_convert_hover_style(config.ui.CARD_NORMAL_STYLE)
    )
    
    # 카드 컨테이너 생성
    return ft.Container(
        content=ft.Column([
            header_row,
            ft.Container(height=8),
            content_text,
            ft.Container(height=8),
            tags_row,
            ft.Container(height=8),
            stats_row,
        ], tight=True),
        width=card_width,
        padding=config.ui.CARD_PADDING,
        margin=config.ui.CARD_MARGIN,
        bgcolor=Colors.WHITE,
        border_radius=config.ui.CARD_BORDER_RADIUS,
        border=ft.border.all(1, Colors.GREY_300),
        shadow=[ft.BoxShadow(
            spread_radius=0,
            blur_radius=4,
            color=Colors.with_opacity(0.1, Colors.BLACK),
            offset=ft.Offset(0, 2)
        )],
        animate=config.ui.ANIMATION_DURATION,
        animate_scale=config.ui.ANIMATION_DURATION,
        on_hover=hover_handler,
        on_click=_create_card_click_wrapper(card_click_handler, stats_controls),
    )


def _get_current_user_id(page: ft.Page) -> str:
    """현재 사용자 ID 조회"""
    try:
        from services.auth_service import get_current_user
        current_user = get_current_user(page)
        return current_user.get("user_id", "") if current_user else ""
    except Exception:
        return ""


def _create_header_row(prompt_data: Dict[str, Any]) -> ft.Row:
    """헤더 행 생성 (썸네일 + 제목 + 뱃지)"""
    title = prompt_data.get("title", "제목 없음")
    max_length = config.business.CARD_TITLE_TRUNCATE
    
    truncated_title = (
        title[:max_length] + "..." 
        if len(title) > max_length 
        else title
    )
    
    return ft.Row([
        create_thumbnail_area(prompt_data),
        ft.Container(width=12),
        ft.Column([
            ft.Text(
                truncated_title,
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


def _create_content_text(prompt_data: Dict[str, Any]) -> ft.Text:
    """컨텐츠 텍스트 생성"""
    content = prompt_data.get("content", "내용이 없습니다.")
    max_length = config.business.CARD_CONTENT_TRUNCATE
    
    truncated_content = (
        content[:max_length] + "..." 
        if len(content) > max_length 
        else content
    )
    
    return ft.Text(
        truncated_content,
        size=12,
        color=Colors.GREY_700,
    )


def _convert_hover_style(style_config: Dict[str, Any]) -> Dict[str, Any]:
    """설정의 스타일을 Flet 컨트롤 속성으로 변환"""
    converted = {}
    
    if 'bgcolor' in style_config:
        converted['bgcolor'] = style_config['bgcolor']
    
    if 'border' in style_config and 'border_color' in style_config:
        # 간단화된 테두리 처리
        converted['border'] = ft.border.all(2, Colors.BLUE_200) if 'BLUE' in str(style_config['border']) else ft.border.all(1, Colors.GREY_300)
    
    if 'scale' in style_config:
        converted['scale'] = style_config['scale']
    
    # 그림자 효과는 별도 처리 필요
    if 'shadow_blur' in style_config:
        converted['shadow'] = [ft.BoxShadow(
            spread_radius=0,
            blur_radius=style_config.get('shadow_blur', 4),
            color=Colors.with_opacity(
                style_config.get('shadow_opacity', 0.1), 
                style_config.get('shadow_color', Colors.BLACK)
            ),
            offset=ft.Offset(0, 2)
        )]
    
    return converted


def _create_card_click_wrapper(card_handler, stats_controls):
    """카드 클릭과 통계 버튼 클릭을 구분하는 래퍼"""
    def wrapper(e):
        # 통계 버튼 클릭인지 확인
        if hasattr(e, 'control') and getattr(e.control, 'data', None) == "event_handled":
            return  # 통계 버튼 클릭이면 상세페이지로 이동하지 않음
        
        # 카드 클릭 처리
        return card_handler(e)
    
    return wrapper


def load_prompt_cards(container: ft.Column, page: ft.Page, page_width: Optional[int] = None):
    """프롬프트 카드 로딩 및 그리드 배치"""
    
    # 반응형 카드 너비 계산을 함수 밖으로 이동
    if page_width is None:
        page_width = getattr(page, 'window_width', 1200)
    
    card_width = config.get_responsive_card_width(page_width)
    
    def _load_cards():
        from services.csv_utils import read_csv_rows
        
        # CSV에서 데이터 로드
        prompts_data = read_csv_rows(Path("data/prompts.csv"))
        
        if not prompts_data:
            container.controls = [ft.Text("프롬프트가 없습니다.", size=16, color=Colors.GREY_600)]
            return
        
        # 최신순 정렬
        prompts_data.sort(key=lambda x: _safe_sort_key(x), reverse=True)
        
        # 카드들 생성
        cards = []
        for prompt in prompts_data:
            card = create_prompt_card(prompt, page, card_width)
            cards.append(card)
        
        # 그리드 배치
        if cards:
            cards_row = ft.Row(
                controls=cards,
                spacing=config.ui.GRID_SPACING,
                alignment=ft.MainAxisAlignment.START,
                wrap=True,
                run_spacing=10,
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
    
    # 직접 실행으로 디버깅
    try:
        _load_cards()
    except Exception as e:
        print(f"[ERROR] 프롬프트 카드 로딩 오류: {e}")
        import traceback
        traceback.print_exc()
        container.controls = [ft.Text(f"카드 로딩 오류: {e}", color=Colors.RED)]


def _safe_sort_key(prompt_data: Dict[str, Any]) -> int:
    """안전한 정렬 키 생성"""
    created_at = prompt_data.get("created_at", "0")
    if not created_at or str(created_at).strip() == "":
        return 0
    try:
        return int(created_at)
    except (ValueError, TypeError):
        return 0
