"""
공통 이벤트 핸들러 패턴
"""
import flet as ft
from typing import Callable, Optional, Any, Tuple
from utils.error_handler import handle_error, ErrorType, ErrorSeverity


def create_stat_handler(
    action_func: Callable[[str, str], Tuple[Any, int]], 
    text_control: ft.Text,
    current_user_id: str,
    prompt_id: str,
    error_msg: str = "처리 중 오류가 발생했습니다.",
    success_callback: Optional[Callable] = None
) -> Callable:
    """
    통계 업데이트 핸들러 팩토리
    
    Args:
        action_func: 실행할 액션 함수 (좋아요, 북마크 등)
        text_control: 업데이트할 텍스트 컨트롤
        current_user_id: 현재 사용자 ID
        prompt_id: 프롬프트 ID
        error_msg: 에러 메시지
        success_callback: 성공 시 실행할 콜백
    
    Returns:
        이벤트 핸들러 함수
    """
    def handler(e):
        try:
            result, total = action_func(current_user_id or "guest", prompt_id)
            text_control.value = str(total)
            text_control.update()
            
            if success_callback:
                success_callback(result, total)
                
        except Exception as ex:
            handle_error(
                error=ex,
                error_type=ErrorType.DATA,
                severity=ErrorSeverity.MEDIUM,
                user_message=error_msg,
                page=getattr(e, 'page', None) if hasattr(e, 'page') else None
            )
    
    return handler


def create_navigation_handler(
    page: ft.Page,
    route: str,
    auth_required: bool = False,
    point_cost: int = 0,
    error_msg: str = "페이지 이동 중 오류가 발생했습니다."
) -> Callable:
    """
    네비게이션 핸들러 팩토리
    
    Args:
        page: Flet 페이지
        route: 이동할 라우트
        auth_required: 인증 필요 여부
        point_cost: 포인트 차감액
        error_msg: 에러 메시지
    
    Returns:
        네비게이션 핸들러 함수
    """
    def handler(e):
        try:
            # 인증 확인
            if auth_required:
                try:
                    from services.auth_service import get_current_user
                except ImportError:
                    # 폴백: 기본 사용자 정보
                    def get_current_user(page):
                        return page.session.get("user")
                
                current_user = get_current_user(page)
                if not current_user or not current_user.get("user_id"):
                    from components.toast import show_toast
                    show_toast(page, "로그인이 필요합니다.", 2000)
                    page.go("/login")
                    return
            
            # 포인트 차감
            if point_cost > 0 and auth_required:
                from services.points_service import try_consume_view
                current_user = get_current_user(page)
                user_id = current_user.get("user_id")
                
                result = try_consume_view(user_id)
                if not result.get("ok"):
                    _show_point_shortage_dialog(page)
                    return
            
            # 네비게이션 실행
            page.go(route)
            
        except Exception as ex:
            handle_error(
                error=ex,
                error_type=ErrorType.UI,
                severity=ErrorSeverity.MEDIUM,
                user_message=error_msg,
                page=page
            )
    
    return handler


def _show_point_shortage_dialog(page: ft.Page):
    """포인트 부족 다이얼로그 표시"""
    def close_dialog(e):
        dialog.open = False
        page.update()
    
    def go_login(e):
        dialog.open = False
        page.go("/login")
    
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("포인트 부족"),
        content=ft.Text("이 프롬프트를 보려면 포인트가 부족합니다. 일일 무료 조회가 소진되었습니다."),
        actions=[
            ft.TextButton("닫기", on_click=close_dialog),
            ft.TextButton("로그인/충전", on_click=go_login),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    page.dialog = dialog
    dialog.open = True
    page.update()


def create_hover_handler(
    hover_style: dict,
    normal_style: dict
) -> Callable:
    """
    호버 효과 핸들러 팩토리
    
    Args:
        hover_style: 호버 시 적용할 스타일
        normal_style: 일반 상태 스타일
    
    Returns:
        호버 이벤트 핸들러
    """
    def handler(e):
        try:
            control = e.control
            is_hover = e.data == "true"
            
            style = hover_style if is_hover else normal_style
            
            # 스타일 적용
            for attr, value in style.items():
                setattr(control, attr, value)
            
            control.update()
            
        except Exception as ex:
            handle_error(
                error=ex,
                error_type=ErrorType.UI,
                severity=ErrorSeverity.LOW,
                user_message=None,  # 호버 에러는 사용자에게 알리지 않음
                show_toast=False
            )
    
    return handler


def create_form_submit_handler(
    validation_func: Callable[[dict], Tuple[bool, str]],
    submit_func: Callable[[dict], bool],
    success_callback: Optional[Callable] = None,
    error_msg: str = "처리 중 오류가 발생했습니다."
) -> Callable:
    """
    폼 제출 핸들러 팩토리
    
    Args:
        validation_func: 유효성 검사 함수
        submit_func: 제출 처리 함수
        success_callback: 성공 시 콜백
        error_msg: 에러 메시지
    
    Returns:
        폼 제출 핸들러
    """
    def handler(e):
        try:
            # 폼 데이터 수집 (구현 필요)
            form_data = {}  # 실제로는 폼에서 데이터 수집
            
            # 유효성 검사
            is_valid, validation_msg = validation_func(form_data)
            if not is_valid:
                handle_error(
                    error=ValueError(validation_msg),
                    error_type=ErrorType.VALIDATION,
                    user_message=validation_msg,
                    page=getattr(e, 'page', None)
                )
                return
            
            # 제출 처리
            success = submit_func(form_data)
            if success and success_callback:
                success_callback()
                
        except Exception as ex:
            handle_error(
                error=ex,
                error_type=ErrorType.DATA,
                severity=ErrorSeverity.MEDIUM,
                user_message=error_msg,
                page=getattr(e, 'page', None)
            )
    
    return handler


def stop_event_propagation(func: Callable) -> Callable:
    """
    이벤트 전파 방지 데코레이터
    
    Args:
        func: 래핑할 함수
    
    Returns:
        이벤트 전파가 방지된 함수
    """
    def wrapper(e):
        try:
            result = func(e)
            # 이벤트 전파 중단
            if hasattr(e, 'control'):
                e.control.data = "event_handled"
            return result
        except Exception as ex:
            handle_error(
                error=ex,
                error_type=ErrorType.UI,
                severity=ErrorSeverity.LOW,
                user_message="이벤트 처리 중 오류가 발생했습니다.",
                page=getattr(e, 'page', None) if hasattr(e, 'page') else None
            )
    
    return wrapper
