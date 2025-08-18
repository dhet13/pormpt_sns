# Promptub global constants - DEPRECATED
# 새로운 코드는 config.app_config를 사용하세요

from config.app_config import config

# 하위 호환성을 위한 레거시 상수들
FREE_VIEWS_PER_DAY = config.business.FREE_VIEWS_PER_DAY
VIEW_COST = config.business.POINT_COST_PER_VIEW

UI_CONSTANTS = {
    "CARD_WIDTH": config.ui.CARD_WIDTH,
    "MAX_CONTENT_WIDTH": config.ui.MAX_CONTENT_WIDTH,
    "SIDEBAR_WIDTH": config.ui.SIDEBAR_WIDTH,
    "GRID_SPACING": config.ui.GRID_SPACING,
    "ANIMATION_DURATION": config.ui.ANIMATION_DURATION,
}

# 드롭다운 옵션들
PLATFORM_OPTIONS = [
    {"key": "gpt4", "label": "ChatGPT"},
    {"key": "claude", "label": "Claude"},
    {"key": "gemini", "label": "Gemini"},
    {"key": "midjourney", "label": "Midjourney"},
    {"key": "dalle", "label": "DALL-E"},
    {"key": "copilot", "label": "Copilot"},
    {"key": "stable_diffusion", "label": "Stable Diffusion"},
]

CATEGORY_OPTIONS = [
    {"key": "텍스트", "label": "📝 텍스트"},
    {"key": "이미지", "label": "🎨 이미지"},
    {"key": "글쓰기", "label": "✍️ 글쓰기"},
    {"key": "개발", "label": "💻 개발"},
    {"key": "마케팅", "label": "📈 마케팅"},
    {"key": "교육", "label": "📚 교육"},
    {"key": "디자인", "label": "🎨 디자인"},
    {"key": "업무", "label": "💼 업무"},
]

"""
promptub 상수 정의의
"""
#AI 모델 정보 (아이콘, 이름, 외부정보)

AI_MODELS = {
    "gpt-4o": {
        "name": "GPT-4o",
        "icon": "🤖",
        "url": "https://chat.openai.com",
        "description": "OpenAI의 최신 모델로, 높은 성능과 정확도를 제공합니다.",
        "corlor": "#10A37F",
    },
        "gpt35": {
        "name": "GPT-3.5",
        "icon": "🤖", 
        "url": "https://chat.openai.com",
        "description": "OpenAI의 대화형 AI",
        "color": "#10A37F"
    },
    "claude": {
        "name": "Claude",
        "icon": "🧠",
        "url": "https://claude.ai",
        "description": "Anthropic의 AI 어시스턴트",
        "color": "#CC785C"
    },
    "clova_x": {
        "name": "CLOVA X",
        "icon": "🇰🇷",
        "url": "https://clova-x.naver.com",
        "description": "네이버의 한국어 특화 AI",
        "color": "#03C75A"
    },
    "gemini": {
        "name": "Gemini",
        "icon": "💎",
        "url": "https://gemini.google.com",
        "description": "Google의 멀티모달 AI",
        "color": "#4285F4"
    },
    "dalle": {
        "name": "DALL-E",
        "icon": "🎨",
        "url": "https://labs.openai.com",
        "description": "OpenAI의 이미지 생성 AI",
        "color": "#FF6B6B"
    },
    "midjourney": {
        "name": "Midjourney",
        "icon": "🖼️",
        "url": "https://midjourney.com",
        "description": "고품질 이미지 생성 AI",
        "color": "#5865F2"
    }
}

#포인트 시스템
POINTS = {
    # 직접 행동 보상
    "prompt_create": 20,
    "comment_create": 3,
    "daily_login": 3,

    # 간접 보상
    "like_received": 3,
    "share_prompt": 5,

    # 마이스톤 보상
    "view_milestone_500":10,
    "view_milestone_1000":25,
    "view_milestone_2000":50,

    # 품질 기반 특별 보상 (수동)
    "featured_prompt": 100,
    "weekly_best":50,

    # 일반 활동 한도
    "daily_limit": 200,
}

VIEWING_SYSTEM = {
    # 무료 조회 한도
    "daily_free_views": 10,
    "new_user_free_views": 10,
    "preview_free": True,

    # 조회 비용
    "basic_view_cost": 2,
    "premium_view_cost": 3,
    "featured_view_cost": 2,

    # 특별 혜택
    "own_prompt_views": True,
    "follower_discount": 0.5,
    "bookmark_refund": 0.5,
}

# 프롬프트 등급 시스템
PROMPT_TIERS = {
    "basic": {
        "tier_name": "일반",
        "cost": 1,
        "requirements": None,
        "color": "#9E9E9E"
    },
    "premium": {
        "tier_name": "프리미엄",
        "cost": 3,
        "requirements": "100+ likes or featured",
        "color": "#FF9800"
    },
    "featured": {
        "tier_name": "추천",
        "cost": 2,
        "requirements": "admin selection",
        "color": "#4CAF50"
    },
}

# 포인트 부족 시 안내
POINT_GUIDANCE = {
    "insufficient_message": "포인트가 부족합니다. 프롬프트를 작성하거나 댓글을 달아 포인트를 획득하세요!",
    "earn_suggestions": [
        "프롬프트 작성 (+20점)",
        "댓글 작성 (+3점)",
        "일일 로그인 (+3점)",
        "다른 사용자 팔로우 (할인 혜택택)",
    ]
}

# 조회 혜택 시스템
VIEWING_BENEFITS = {
    "level_bonus_views": {
        "Contributor": 5,    # 레벨업시 무료 조회 +5개
        "Influencer": 10,    # 무료 조회 +10개  
        "Master": 15,        # 무료 조회 +15개
        "Legend": 20,        # 무료 조회 +20개
    },
    "weekly_bonus": 20,      # 주간 보너스 무료 조회
    "streak_bonus": {        # 연속 로그인 보너스
        "7days": 10,         # 7일 연속시 +10개 무료 조회
        "30days": 50,        # 30일 연속시 +50개 무료 조회
    }
}

# 사용자 레벨 (기존에 없다면 추가)
USER_LEVELS = {
    1: "Rookie",        # 0-99점
    100: "Contributor", # 100-499점
    500: "Influencer",  # 500-1999점  
    2000: "Master",     # 2000-9999점
    10000: "Legend"     # 10000점+
}

# === 소셜 로그인 설정 (추후 구현) ===
# SOCIAL_LOGIN_PROVIDERS = {
#     "google": {
#         "name": "Google",
#         "icon": "🔍",
#         "color": "#DB4437",
#         "client_id": "your_google_client_id",
#         "client_secret": "your_google_client_secret",
#         "scope": ["email", "profile"],
#         "auth_url": "https://accounts.google.com/o/oauth2/auth"
#     },
#     "kakao": {
#         "name": "카카오",
#         "icon": "💛", 
#         "color": "#FEE500",
#         "client_id": "your_kakao_client_id",
#         "client_secret": "your_kakao_client_secret",
#         "auth_url": "https://kauth.kakao.com/oauth/authorize"
#     },
#     "naver": {
#         "name": "네이버",
#         "icon": "🟢",
#         "color": "#03C75A", 
#         "client_id": "your_naver_client_id",
#         "client_secret": "your_naver_client_secret",
#         "auth_url": "https://nid.naver.com/oauth2.0/authorize"
#     },
#     "github": {
#         "name": "GitHub",
#         "icon": "🐙",
#         "color": "#333333",
#         "client_id": "your_github_client_id", 
#         "client_secret": "your_github_client_secret",
#         "auth_url": "https://github.com/login/oauth/authorize"
#     }
# }

# # 소셜 로그인 보너스 포인트
# SOCIAL_LOGIN_BONUS = {
#     "first_social_login": 30,      # 첫 소셜 로그인시 보너스
#     "account_linking": 20,         # 기존 계정에 소셜 연동시
#     "profile_completion": 10,      # 소셜 프로필 정보 동기화시
# }