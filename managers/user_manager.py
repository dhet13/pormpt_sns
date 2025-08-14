"""
사용자 데이터 매니저
"""
from pathlib import Path
from typing import List, Optional
from managers.base_manager import BaseManager
from models.user import User
from config.settings import CSV_FILES

class UserManager(BaseManager[User]):
    """사용자 데이터 관리 클래스"""
    
    def __init__(self):
        super().__init__(CSV_FILES["users"])
    
    def get_fieldnames(self) -> List[str]:
        """CSV 파일의 컬럼명 리스트 반환"""
        return [
            'user_id', 'username', 'email', 'password_hash',
            'profile_image', 'bio', 'points', 'level',
            'total_prompts', 'total_likes_received', 
            'follower_count', 'following_count',
            'daily_free_views_used', 'last_login', 'login_streak',
            'created_at', 'updated_at', 'status'
        ]
    
    def dict_to_model(self, data: dict) -> User:
        """딕셔너리를 User 객체로 변환"""
        return User.from_dict(data)
    
    def model_to_dict(self, model: User) -> dict:
        """User 객체를 딕셔너리로 변환"""
        return model.to_dict()
    
    # === 사용자 특화 메서드들 ===
    
    def find_by_email(self, email: str) -> Optional[User]:
        """이메일로 사용자 찾기"""
        users = self.filter(email=email)
        return users[0] if users else None
    
    def find_by_username(self, username: str) -> Optional[User]:
        """사용자명으로 찾기"""
        users = self.filter(username=username)
        return users[0] if users else None
    
    def is_email_taken(self, email: str) -> bool:
        """이메일 중복 확인"""
        return self.find_by_email(email) is not None
    
    def is_username_taken(self, username: str) -> bool:
        """사용자명 중복 확인"""
        return self.find_by_username(username) is not None
    
    def update_points(self, user_id: str, points_change: int) -> bool:
        """포인트 업데이트"""
        user = self.find_by_id(user_id, "user_id")
        if user:
            user.points += points_change
            user.points = max(0, user.points)  # 포인트는 0 이하로 떨어지지 않음
            return self.update(user, "user_id")
        return False
    
    def reset_daily_free_views(self, user_id: str) -> bool:
        """일일 무료 조회 횟수 리셋"""
        user = self.find_by_id(user_id, "user_id")
        if user:
            user.daily_free_views_used = 0
            return self.update(user, "user_id")
        return False
    
    def get_top_users_by_points(self, limit: int = 10) -> List[User]:
        """포인트 상위 사용자들"""
        all_users = self.load_all()
        return sorted(all_users, key=lambda u: u.points, reverse=True)[:limit]
    
    def get_active_users(self) -> List[User]:
        """활성 사용자들만 조회"""
        return self.filter(status="active")