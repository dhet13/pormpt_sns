"""
구조화된 에러 핸들링 시스템
"""
import flet as ft
from enum import Enum
from typing import Optional, Callable, Any
import logging
from datetime import datetime

# 로거 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ErrorType(Enum):
    """에러 유형 분류"""
    NETWORK = "network"
    DATA = "data"
    AUTH = "auth"
    UI = "ui"
    VALIDATION = "validation"
    PERMISSION = "permission"


class ErrorSeverity(Enum):
    """에러 심각도"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


def handle_error(
    error: Exception,
    error_type: ErrorType,
    severity: ErrorSeverity = ErrorSeverity.MEDIUM,
    user_message: Optional[str] = None,
    page: Optional[ft.Page] = None,
    show_toast: bool = True,
    callback: Optional[Callable] = None
) -> None:
    """
    구조화된 에러 처리
    
    Args:
        error: 발생한 예외
        error_type: 에러 유형
        severity: 심각도
        user_message: 사용자에게 표시할 메시지
        page: Flet 페이지 객체
        show_toast: 토스트 메시지 표시 여부
        callback: 에러 처리 후 실행할 콜백 함수
    """
    
    # 1. 로깅
    log_message = f"[{error_type.value.upper()}] {str(error)}"
    
    if severity == ErrorSeverity.CRITICAL:
        logger.critical(log_message)
    elif severity == ErrorSeverity.HIGH:
        logger.error(log_message)
    elif severity == ErrorSeverity.MEDIUM:
        logger.warning(log_message)
    else:
        logger.info(log_message)
    
    # 2. 사용자 알림
    if user_message and page and show_toast:
        try:
            from components.toast import show_toast as toast_func
            toast_func(page, user_message, 3000)
        except Exception:
            # 토스트 실패 시 스낵바로 폴백
            try:
                page.snack_bar = ft.SnackBar(
                    ft.Text(user_message),
                    open=True,
                    duration=3000
                )
                page.update()
            except Exception:
                pass
    
    # 3. 콜백 실행
    if callback:
        try:
            callback()
        except Exception as callback_error:
            logger.error(f"Error in callback: {callback_error}")


def safe_execute(
    func: Callable,
    error_type: ErrorType,
    user_message: str = "작업 중 오류가 발생했습니다.",
    page: Optional[ft.Page] = None,
    default_return: Any = None,
    **kwargs
) -> Any:
    """
    안전한 함수 실행 래퍼
    
    Args:
        func: 실행할 함수
        error_type: 에러 유형
        user_message: 에러 시 사용자 메시지
        page: Flet 페이지
        default_return: 에러 시 반환할 기본값
        **kwargs: 에러 핸들러에 전달할 추가 인자
    
    Returns:
        함수 실행 결과 또는 기본값
    """
    try:
        return func()
    except Exception as e:
        handle_error(
            error=e,
            error_type=error_type,
            user_message=user_message,
            page=page,
            **kwargs
        )
        return default_return


def create_error_handler(
    error_type: ErrorType,
    user_message: str = "작업 중 오류가 발생했습니다.",
    severity: ErrorSeverity = ErrorSeverity.MEDIUM
) -> Callable:
    """
    에러 핸들러 팩토리 함수
    
    Returns:
        에러 핸들링이 포함된 데코레이터
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # page 객체 찾기 (일반적으로 첫 번째 인자)
                page = None
                if args and hasattr(args[0], 'update'):
                    page = args[0]
                elif 'page' in kwargs:
                    page = kwargs['page']
                
                handle_error(
                    error=e,
                    error_type=error_type,
                    severity=severity,
                    user_message=user_message,
                    page=page
                )
                return None
        return wrapper
    return decorator


# 자주 사용되는 에러 핸들러들
auth_error_handler = create_error_handler(
    ErrorType.AUTH, 
    "인증 중 오류가 발생했습니다.",
    ErrorSeverity.HIGH
)

data_error_handler = create_error_handler(
    ErrorType.DATA,
    "데이터 처리 중 오류가 발생했습니다.",
    ErrorSeverity.MEDIUM
)

ui_error_handler = create_error_handler(
    ErrorType.UI,
    "화면 업데이트 중 오류가 발생했습니다.",
    ErrorSeverity.LOW
)

validation_error_handler = create_error_handler(
    ErrorType.VALIDATION,
    "입력값을 확인해주세요.",
    ErrorSeverity.MEDIUM
)
