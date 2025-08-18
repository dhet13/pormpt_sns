"""
프로젝트 전체에서 사용하는 타입 힌트 정의
"""
from typing import Dict, List, Optional, Union, Any, Callable, Tuple, TypeVar, Generic
from dataclasses import dataclass
import flet as ft

# 기본 타입 별칭
UserID = str
PromptID = str
CategoryID = str
AIModelKey = str
TagString = str
PointsValue = int
TimestampValue = Union[int, str]

# 딕셔너리 타입 별칭
PromptData = Dict[str, Any]
UserData = Dict[str, Any]
ConfigData = Dict[str, Any]
InteractionData = Dict[str, Any]

# 함수 타입 별칭
EventHandler = Callable[[ft.ControlEvent], None]
ValidationFunc = Callable[[Dict[str, Any]], Tuple[bool, str]]
ActionFunc = Callable[[str, str], Tuple[Any, int]]
ErrorCallback = Optional[Callable[[], None]]

# 제네릭 타입
T = TypeVar('T')
DataModel = TypeVar('DataModel')

# 응답 타입들
@dataclass
class ServiceResponse(Generic[T]):
    """서비스 레이어 응답 타입"""
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None
    message: Optional[str] = None

@dataclass
class ValidationResult:
    """유효성 검사 결과"""
    is_valid: bool
    message: str
    errors: Optional[Dict[str, str]] = None

@dataclass
class PaginationResult(Generic[T]):
    """페이지네이션 결과"""
    items: List[T]
    total: int
    page: int
    per_page: int
    total_pages: int
    has_next: bool
    has_prev: bool

@dataclass
class PointsTransaction:
    """포인트 거래 정보"""
    user_id: UserID
    amount: int
    transaction_type: str  # 'earn', 'spend', 'bonus'
    description: str
    timestamp: TimestampValue

@dataclass
class InteractionResult:
    """상호작용 결과 (좋아요, 북마크 등)"""
    success: bool
    new_state: bool  # True: 활성화, False: 비활성화
    total_count: int
    message: Optional[str] = None

# UI 관련 타입
@dataclass
class CardStyle:
    """카드 스타일 정보"""
    bgcolor: str
    border_color: str
    border_width: int
    shadow_blur: int
    shadow_color: str
    shadow_opacity: float
    scale: float

@dataclass
class ResponsiveBreakpoints:
    """반응형 브레이크포인트"""
    mobile: int = 480
    tablet: int = 768
    desktop: int = 1024
    large: int = 1200

# 설정 관련 타입
@dataclass
class DatabaseConnection:
    """데이터베이스 연결 정보"""
    type: str  # 'csv', 'sqlite', 'postgresql'
    path: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    database: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None

# 에러 관련 타입
@dataclass
class ErrorContext:
    """에러 컨텍스트 정보"""
    user_id: Optional[UserID] = None
    prompt_id: Optional[PromptID] = None
    action: Optional[str] = None
    additional_info: Optional[Dict[str, Any]] = None

# CSV 관련 타입
CSVRow = Dict[str, str]
CSVData = List[CSVRow]
CSVFieldNames = List[str]

# 필터 및 정렬 타입
@dataclass
class FilterCriteria:
    """필터 조건"""
    category: Optional[CategoryID] = None
    ai_model: Optional[AIModelKey] = None
    tags: Optional[List[str]] = None
    user_id: Optional[UserID] = None
    min_likes: Optional[int] = None
    max_likes: Optional[int] = None
    date_from: Optional[TimestampValue] = None
    date_to: Optional[TimestampValue] = None

@dataclass
class SortCriteria:
    """정렬 조건"""
    field: str
    ascending: bool = True

# 검색 관련 타입
@dataclass
class SearchQuery:
    """검색 쿼리"""
    keyword: str
    filters: Optional[FilterCriteria] = None
    sort: Optional[SortCriteria] = None
    page: int = 1
    per_page: int = 12

@dataclass
class SearchResult(Generic[T]):
    """검색 결과"""
    query: SearchQuery
    results: PaginationResult[T]
    suggestions: Optional[List[str]] = None
    took_ms: Optional[int] = None

# 인증 관련 타입
@dataclass
class AuthCredentials:
    """인증 자격증명"""
    username: Optional[str] = None
    email: Optional[str] = None
    password: str = ""

@dataclass
class AuthResult:
    """인증 결과"""
    success: bool
    user_data: Optional[UserData] = None
    token: Optional[str] = None
    expires_at: Optional[TimestampValue] = None
    error: Optional[str] = None

# 통계 관련 타입
@dataclass
class PromptStats:
    """프롬프트 통계"""
    views: int = 0
    likes: int = 0
    bookmarks: int = 0
    shares: int = 0
    comments: int = 0

@dataclass
class UserStats:
    """사용자 통계"""
    total_prompts: int = 0
    total_likes_received: int = 0
    total_views_received: int = 0
    points: int = 0
    level: int = 1
    streak_days: int = 0

# 알림 관련 타입
@dataclass
class Notification:
    """알림 정보"""
    id: str
    user_id: UserID
    title: str
    message: str
    type: str  # 'info', 'success', 'warning', 'error'
    read: bool = False
    created_at: TimestampValue = 0
    expires_at: Optional[TimestampValue] = None
