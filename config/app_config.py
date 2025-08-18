"""
애플리케이션 설정 관리 (dataclass 기반)
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List
from flet import Colors
import os


@dataclass
class UIConfig:
    """UI 관련 설정"""
    # 카드 레이아웃
    CARD_WIDTH: int = 280
    CARD_MIN_WIDTH: int = 250
    CARD_MAX_WIDTH: int = 600
    GRID_SPACING: int = 12
    CARD_PADDING: int = 12
    CARD_MARGIN: int = 6
    CARD_BORDER_RADIUS: int = 12
    
    # 레이아웃
    SIDEBAR_WIDTH: int = 200
    MAX_CONTENT_WIDTH: int = 1400
    HEADER_HEIGHT: int = 80
    
    # 반응형 브레이크포인트
    BREAKPOINT_LARGE: int = 1000  # 3열 그리드
    BREAKPOINT_MEDIUM: int = 550  # 2열 그리드
    
    # 애니메이션
    ANIMATION_DURATION: int = 200
    HOVER_SCALE: float = 1.02
    
    # 색상 테마
    PRIMARY_COLOR: str = Colors.BLUE_700
    SECONDARY_COLOR: str = Colors.GREY_600
    SUCCESS_COLOR: str = Colors.GREEN_600
    ERROR_COLOR: str = Colors.RED_600
    WARNING_COLOR: str = Colors.ORANGE_600
    
    # 카드 호버 효과
    CARD_HOVER_STYLE: Dict[str, Any] = field(default_factory=lambda: {
        'bgcolor': Colors.BLUE_50,
        'border': f'2px solid {Colors.BLUE_200}',
        'scale': 1.02,
        'shadow_blur': 12,
        'shadow_color': Colors.BLUE_400,
        'shadow_opacity': 0.15
    })
    
    CARD_NORMAL_STYLE: Dict[str, Any] = field(default_factory=lambda: {
        'bgcolor': Colors.WHITE,
        'border': f'1px solid {Colors.GREY_300}',
        'scale': 1.0,
        'shadow_blur': 4,
        'shadow_color': Colors.BLACK,
        'shadow_opacity': 0.1
    })


@dataclass
class BusinessConfig:
    """비즈니스 로직 관련 설정"""
    # 포인트 시스템
    FREE_VIEWS_PER_DAY: int = 10
    POINT_COST_PER_VIEW: int = 1
    POINTS_FOR_PROMPT_CREATE: int = 50
    POINTS_FOR_LIKE_RECEIVED: int = 5
    POINTS_FOR_COMMENT: int = 3
    POINTS_FOR_SHARE: int = 10
    POINTS_FOR_DAILY_LOGIN: int = 5
    DAILY_POINT_LIMIT: int = 300
    
    # 컨텐츠 제한
    MAX_TITLE_LENGTH: int = 100
    MAX_CONTENT_LENGTH: int = 2000
    MAX_DESCRIPTION_LENGTH: int = 500
    MAX_TAGS_COUNT: int = 10
    MAX_TAG_LENGTH: int = 20
    
    # 표시 제한
    MAX_TAGS_DISPLAY: int = 3
    CARD_TITLE_TRUNCATE: int = 30
    CARD_CONTENT_TRUNCATE: int = 80
    
    # 페이지네이션
    DEFAULT_PAGE_SIZE: int = 12
    MAX_PAGE_SIZE: int = 50


@dataclass
class CategoryConfig:
    """카테고리별 설정"""
    CATEGORIES: Dict[str, Dict[str, str]] = field(default_factory=lambda: {
        "텍스트": {"emoji": "📝", "color": Colors.BLUE_100, "text_color": Colors.BLUE_800},
        "이미지": {"emoji": "🎨", "color": Colors.PURPLE_100, "text_color": Colors.PURPLE_800},
        "글쓰기": {"emoji": "✍️", "color": Colors.GREEN_100, "text_color": Colors.GREEN_800},
        "개발": {"emoji": "💻", "color": Colors.ORANGE_100, "text_color": Colors.ORANGE_800},
        "마케팅": {"emoji": "📈", "color": Colors.RED_100, "text_color": Colors.RED_800},
        "교육": {"emoji": "📚", "color": Colors.INDIGO_100, "text_color": Colors.INDIGO_800},
        "디자인": {"emoji": "🎨", "color": Colors.PINK_100, "text_color": Colors.PINK_800},
        "업무": {"emoji": "💼", "color": Colors.BROWN_100, "text_color": Colors.BROWN_800},
    })
    
    DEFAULT_CATEGORY: Dict[str, str] = field(default_factory=lambda: {
        "emoji": "📝", "color": Colors.GREY_100, "text_color": Colors.GREY_800
    })


@dataclass
class AIModelConfig:
    """AI 모델별 설정"""
    AI_MODELS: Dict[str, Dict[str, str]] = field(default_factory=lambda: {
        "gpt4": {"label": "ChatGPT", "color": Colors.GREEN_100, "text_color": Colors.GREEN_800},
        "claude": {"label": "Claude", "color": Colors.ORANGE_100, "text_color": Colors.ORANGE_800},
        "gemini": {"label": "Gemini", "color": Colors.BLUE_100, "text_color": Colors.BLUE_800},
        "midjourney": {"label": "MJ", "color": Colors.PURPLE_100, "text_color": Colors.PURPLE_800},
        "dalle": {"label": "DALL-E", "color": Colors.PINK_100, "text_color": Colors.PINK_800},
        "copilot": {"label": "Copilot", "color": Colors.INDIGO_100, "text_color": Colors.INDIGO_800},
        "stable_diffusion": {"label": "SD", "color": Colors.TEAL_100, "text_color": Colors.TEAL_800},
    })
    
    DEFAULT_MODEL: Dict[str, str] = field(default_factory=lambda: {
        "label": "Unknown", "color": Colors.GREY_100, "text_color": Colors.GREY_800
    })


@dataclass
class DatabaseConfig:
    """데이터베이스 관련 설정"""
    # CSV 파일 경로
    BASE_DIR: str = field(default_factory=lambda: os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    def __post_init__(self):
        """초기화 후 처리"""
        self.DATA_DIR = os.path.join(self.BASE_DIR, "data")
        self.CSV_FILES = {
            "prompts": os.path.join(self.DATA_DIR, "prompts.csv"),
            "users": os.path.join(self.DATA_DIR, "users.csv"),
            "comments": os.path.join(self.DATA_DIR, "comments.csv"),
            "interactions": os.path.join(self.DATA_DIR, "interactions.csv"),
        }
    
    # CSV 필드 정의
    PROMPT_FIELDS: List[str] = field(default_factory=lambda: [
        "prompt_id", "user_id", "title", "content", "category", "ai_model_key",
        "tags", "likes", "bookmarks", "shares", "comments", "views", 
        "created_at", "updated_at"
    ])
    
    USER_FIELDS: List[str] = field(default_factory=lambda: [
        "user_id", "username", "email", "password_hash", "points", 
        "level", "created_at", "last_login"
    ])


@dataclass
class SecurityConfig:
    """보안 관련 설정"""
    # 세션
    SESSION_TIMEOUT: int = 3600  # 1시간
    
    # 비밀번호
    MIN_PASSWORD_LENGTH: int = 8
    REQUIRE_SPECIAL_CHARS: bool = True
    
    # API 제한
    MAX_REQUESTS_PER_MINUTE: int = 60
    MAX_LOGIN_ATTEMPTS: int = 5


@dataclass
class LoggingConfig:
    """로깅 설정"""
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "app.log"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    MAX_LOG_SIZE: int = 10 * 1024 * 1024  # 10MB
    BACKUP_COUNT: int = 5


@dataclass
class AppConfig:
    """전체 애플리케이션 설정"""
    # 앱 정보
    APP_NAME: str = "Promptub"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "AI 프롬프트 공유 SNS"
    
    # 서버 설정
    DEFAULT_PORT: int = 8000
    DEFAULT_HOST: str = "0.0.0.0"
    DEBUG: bool = field(default_factory=lambda: os.getenv("DEBUG", "False").lower() == "true")
    
    # 하위 설정들
    ui: UIConfig = field(default_factory=UIConfig)
    business: BusinessConfig = field(default_factory=BusinessConfig)
    category: CategoryConfig = field(default_factory=CategoryConfig)
    ai_model: AIModelConfig = field(default_factory=AIModelConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    
    def get_category_config(self, category: str) -> Dict[str, str]:
        """카테고리 설정 조회"""
        return self.category.CATEGORIES.get(category, self.category.DEFAULT_CATEGORY)
    
    def get_ai_model_config(self, model_key: str) -> Dict[str, str]:
        """AI 모델 설정 조회"""
        return self.ai_model.AI_MODELS.get(model_key, self.ai_model.DEFAULT_MODEL)
    
    def get_responsive_card_width(self, page_width: int) -> int:
        """반응형 카드 너비 계산"""
        sidebar_width = self.ui.SIDEBAR_WIDTH if page_width >= self.ui.BREAKPOINT_LARGE else 0
        content_padding = 40
        available_width = page_width - sidebar_width - content_padding
        
        if available_width >= 800:  # 3열
            card_width = (available_width - 24) // 3
        elif available_width >= self.ui.BREAKPOINT_MEDIUM:  # 2열
            card_width = (available_width - 12) // 2
        else:  # 1열
            card_width = min(available_width - 20, 400)
        
        return max(self.ui.CARD_MIN_WIDTH, min(card_width, self.ui.CARD_MAX_WIDTH))


# 전역 설정 인스턴스
config = AppConfig()
