"""
프롬프트 데이터 모델
"""
from datetime import datetime
from typing import Optional, List
from dataclasses import dataclass

@dataclass
class PromptCard:
    prompt_id: str
    user_id: str
    title: str
    content: str
    description: str
    category_id: int
    ai_model_key: str  # AI_MODELS의 키값
    tags: List[str]
    tier: str = "basic"  # basic, premium, featured
    difficulty_level: int = 1  # 1: 초급, 2: 중급, 3: 고급
    views: int = 0
    likes: int = 0
    bookmarks: int = 0
    shares: int = 0
    comments_count: int = 0
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    status: str = "published"  # draft, published, featured, archived, reported
    
    def get_view_cost(self) -> int:
        """프롬프트 조회 비용 반환"""
        from config.constants import VIEWING_SYSTEM
        if self.tier == "basic":
            return VIEWING_SYSTEM["basic_view_cost"]
        elif self.tier == "premium":
            return VIEWING_SYSTEM["premium_view_cost"]
        elif self.tier == "featured":
            return VIEWING_SYSTEM["featured_view_cost"]
        return VIEWING_SYSTEM["basic_view_cost"]
    
    def get_ai_model_info(self) -> dict:
        """AI 모델 정보 반환"""
        from config.constants import AI_MODELS
        return AI_MODELS.get(self.ai_model_key, {})
    
    def get_category_info(self) -> dict:
        """카테고리 정보 반환"""
        from config.constants import CATEGORIES
        for category in CATEGORIES:
            if category["id"] == self.category_id:
                return category
        return {}
    
    def to_dict(self) -> dict:
        """딕셔너리로 변환 (CSV 저장용)"""
        return {
            'prompt_id': self.prompt_id,
            'user_id': self.user_id,
            'title': self.title,
            'content': self.content,
            'description': self.description,
            'category_id': self.category_id,
            'ai_model_key': self.ai_model_key,
            'tags': ','.join(self.tags),  # 리스트를 문자열로 변환
            'tier': self.tier,
            'difficulty_level': self.difficulty_level,
            'views': self.views,
            'likes': self.likes,
            'bookmarks': self.bookmarks,
            'shares': self.shares,
            'comments_count': self.comments_count,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'status': self.status
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'PromptCard':
        """딕셔너리에서 객체 생성 (CSV 로드용)"""
        return cls(
            prompt_id=data['prompt_id'],
            user_id=data['user_id'],
            title=data['title'],
            content=data['content'],
            description=data['description'],
            category_id=int(data['category_id']),
            ai_model_key=data['ai_model_key'],
            tags=data['tags'].split(',') if data['tags'] else [],
            tier=data['tier'],
            difficulty_level=int(data['difficulty_level']),
            views=int(data['views']),
            likes=int(data['likes']),
            bookmarks=int(data['bookmarks']),
            shares=int(data['shares']),
            comments_count=int(data['comments_count']),
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at']),
            status=data['status']
        )