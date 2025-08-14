"""
사용자 데이터 모델
"""
from datetime import datetime
from typing import Optional, List
from dataclasses import dataclass

@dataclass
class User:
    user_id: str
    username: str
    email: str
    password_hash: str
    profile_image: Optional[str] = None
    bio: Optional[str] = None
    points: int = 0
    level: int = 1
    total_prompts: int = 0
    total_likes_received: int = 0
    follower_count: int = 0
    following_count: int = 0
    daily_free_views_used: int = 0
    last_login: Optional[datetime] = None
    login_streak: int = 0
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    status: str = "active"  # active, inactive, banned, pending
    
    def get_level_name(self) -> str:
        """레벨에 따른 이름 반환"""
        from config.constants import USER_LEVELS
        for min_points, level_name in sorted(USER_LEVELS.items(), reverse=True):
            if self.points >= min_points:
                return level_name
        return "Rookie"
    
    def get_daily_free_views(self) -> int:
        """레벨에 따른 일일 무료 조회수 반환"""
        from config.constants import VIEWING_SYSTEM, VIEWING_BENEFITS
        base_views = VIEWING_SYSTEM["daily_free_views"]
        level_name = self.get_level_name()
        bonus_views = VIEWING_BENEFITS["level_bonus_views"].get(level_name, 0)
        return base_views + bonus_views
    
    def can_view_prompt(self, cost: int) -> bool:
        """프롬프트 조회 가능 여부 확인"""
        if self.daily_free_views_used < self.get_daily_free_views():
            return True
        return self.points >= cost
    
    def to_dict(self) -> dict:
        """딕셔너리로 변환 (CSV 저장용)"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash,
            'profile_image': self.profile_image or '',
            'bio': self.bio or '',
            'points': self.points,
            'level': self.level,
            'total_prompts': self.total_prompts,
            'total_likes_received': self.total_likes_received,
            'follower_count': self.follower_count,
            'following_count': self.following_count,
            'daily_free_views_used': self.daily_free_views_used,
            'last_login': self.last_login.isoformat() if self.last_login else '',
            'login_streak': self.login_streak,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'status': self.status
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """딕셔너리에서 객체 생성 (CSV 로드용)"""
        return cls(
            user_id=data['user_id'],
            username=data['username'],
            email=data['email'],
            password_hash=data['password_hash'],
            profile_image=data['profile_image'] if data['profile_image'] else None,
            # === 소셜 로그인 관련 필드 (추후 구현) ===
            # social_provider: Optional[str] = None      # "google", "kakao", "naver", "github"
            # social_id: Optional[str] = None            # 소셜 플랫폼의 고유 ID
            # social_profile_url: Optional[str] = None   # 소셜 프로필 이미지 URL
            # is_social_user: bool = False               # 소셜 로그인 사용자 여부
            bio=data['bio'] if data['bio'] else None,
            points=int(data['points']),
            level=int(data['level']),
            total_prompts=int(data['total_prompts']),
            total_likes_received=int(data['total_likes_received']),
            follower_count=int(data['follower_count']),
            following_count=int(data['following_count']),
            daily_free_views_used=int(data['daily_free_views_used']),
            last_login=datetime.fromisoformat(data['last_login']) if data['last_login'] else None,
            login_streak=int(data['login_streak']),
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at']),
            status=data['status']
            # === 소셜 로그인 관련 메서드 (추후 구현) ===
            # def is_google_user(self) -> bool:
            #     """구글 로그인 사용자인지 확인"""
            #     return self.social_provider == "google"
            
            # def is_kakao_user(self) -> bool:
            #     """카카오 로그인 사용자인지 확인"""
            #     return self.social_provider == "kakao"
            
            # def get_social_profile_image(self) -> Optional[str]:
            #     """소셜 프로필 이미지 URL 반환"""
            #     return self.social_profile_url if self.is_social_user else None
            
            # def link_social_account(self, provider: str, social_id: str, profile_url: str = None):
            #     """기존 계정에 소셜 계정 연동"""
            #     self.social_provider = provider
            #     self.social_id = social_id
            #     self.social_profile_url = profile_url
            #     self.is_social_user = True
            #     self.updated_at = datetime.now()
        )