"""
프롬프트 카드 통계 컴포넌트
"""
import flet as ft
from flet import Colors
from typing import Callable, Optional
from ..common_handlers import create_stat_handler, stop_event_propagation
from utils.error_handler import safe_execute, ErrorType


def create_stats_controls(
    prompt_data: dict,
    current_user_id: str,
    page: ft.Page
) -> dict:
    """통계 컨트롤들 생성"""
    prompt_id = str(prompt_data.get("prompt_id") or prompt_data.get("id") or "")
    
    # 텍스트 컨트롤들
    stats_texts = {
        'likes': ft.Text(str(prompt_data.get("likes", "0")), size=11, color=Colors.GREY_600),
        'shares': ft.Text(str(prompt_data.get("shares", "0")), size=11, color=Colors.GREY_600),
        'comments': ft.Text(str(prompt_data.get("comments", "0")), size=11, color=Colors.GREY_600),
        'bookmarks': ft.Text(str(prompt_data.get("bookmarks", "0")), size=11, color=Colors.GREY_600),
        'views': ft.Text(str(prompt_data.get("views", "0")), size=11, color=Colors.GREY_600),
    }
    
    # 핸들러들 생성
    handlers = _create_stat_handlers(stats_texts, current_user_id, prompt_id, page)
    
    # 클러스터들 생성
    clusters = {
        'like': _create_stat_cluster("❤️", stats_texts['likes'], handlers['like']),
        'share': _create_stat_cluster("📤", stats_texts['shares'], handlers['share']),
        'comment': _create_stat_cluster("💬", stats_texts['comments'], None),  # 읽기 전용
        'bookmark': _create_stat_cluster("🔖", stats_texts['bookmarks'], handlers['bookmark']),
        'views': _create_stat_cluster("👁️", stats_texts['views'], None),  # 읽기 전용
    }
    
    return {
        'texts': stats_texts,
        'handlers': handlers,
        'clusters': clusters
    }


def _create_stat_handlers(
    stats_texts: dict,
    current_user_id: str,
    prompt_id: str,
    page: ft.Page
) -> dict:
    """통계 핸들러들 생성"""
    from services.interactions_service import toggle_like, toggle_bookmark, record_share
    
    handlers = {}
    
    # 좋아요 핸들러
    handlers['like'] = create_stat_handler(
        action_func=toggle_like,
        text_control=stats_texts['likes'],
        current_user_id=current_user_id,
        prompt_id=prompt_id,
        error_msg="좋아요 처리 중 오류가 발생했습니다."
    )
    
    # 공유 핸들러
    def share_action(user_id: str, prompt_id: str):
        total = record_share(user_id, prompt_id)
        return True, total  # 공유는 항상 성공으로 처리
    
    handlers['share'] = create_stat_handler(
        action_func=share_action,
        text_control=stats_texts['shares'],
        current_user_id=current_user_id,
        prompt_id=prompt_id,
        error_msg="공유 처리 중 오류가 발생했습니다."
    )
    
    # 북마크 핸들러
    handlers['bookmark'] = create_stat_handler(
        action_func=toggle_bookmark,
        text_control=stats_texts['bookmarks'],
        current_user_id=current_user_id,
        prompt_id=prompt_id,
        error_msg="북마크 처리 중 오류가 발생했습니다."
    )
    
    return handlers


def _create_stat_cluster(
    icon: str, 
    text_control: ft.Text, 
    handler: Optional[Callable] = None
) -> ft.Container:
    """통계 클러스터 생성"""
    content = ft.Row([
        ft.Text(icon, size=10), 
        text_control
    ], spacing=2, tight=True)
    
    cluster = ft.Container(
        content=content,
        padding=ft.padding.symmetric(horizontal=3, vertical=2),
        border_radius=4,
    )
    
    if handler:
        cluster.on_click = stop_event_propagation(handler)
    
    return cluster


def create_stats_row(stats_controls: dict) -> ft.Row:
    """통계 행 생성"""
    clusters = stats_controls['clusters']
    
    return ft.Row([
        clusters['like'],
        ft.Container(width=8),
        clusters['share'],
        ft.Container(width=8),
        clusters['comment'],
        ft.Container(width=8),
        clusters['bookmark'],
        ft.Container(width=8),
        clusters['views'],
    ], tight=True)
