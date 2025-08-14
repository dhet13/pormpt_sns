"""
프롬프트 데이터 매니저
"""
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from managers.base_manager import BaseManager
from models.prompt_card import PromptCard
from config.settings import CSV_FILES

class PromptManager(BaseManager[PromptCard]):
    """프롬프트 데이터 관리 클래스"""
    
    def __init__(self):
        super().__init__(CSV_FILES["prompts"])
    
    def get_fieldnames(self) -> List[str]:
        """CSV 파일의 컬럼명 리스트 반환"""
        return [
            'prompt_id', 'user_id', 'title', 'content', 'description',
            'category_id', 'ai_model_key', 'tags', 'tier', 'difficulty_level',
            'views', 'likes', 'bookmarks', 'shares', 'comments_count',
            'created_at', 'updated_at', 'status'
        ]
    
    def dict_to_model(self, data: dict) -> PromptCard:
        """딕셔너리를 PromptCard 객체로 변환"""
        return PromptCard.from_dict(data)
    
    def model_to_dict(self, model: PromptCard) -> dict:
        """PromptCard 객체를 딕셔너리로 변환"""
        return model.to_dict()
    
    # === 프롬프트 특화 메서드들 ===
    
    def get_by_category(self, category_id: int) -> List[PromptCard]:
        """카테고리별 프롬프트 조회"""
        return self.filter(category_id=category_id, status="published")
    
    def get_by_user(self, user_id: str) -> List[PromptCard]:
        """사용자별 프롬프트 조회"""
        return self.filter(user_id=user_id)
    
    def get_by_ai_model(self, ai_model_key: str) -> List[PromptCard]:
        """AI 모델별 프롬프트 조회"""
        return self.filter(ai_model_key=ai_model_key, status="published")
    
    def get_published_prompts(self) -> List[PromptCard]:
        """게시된 프롬프트만 조회"""
        return self.filter(status="published")
    
    def get_featured_prompts(self) -> List[PromptCard]:
        """추천 프롬프트 조회"""
        return self.filter(tier="featured", status="published")
    
    def get_popular_prompts(self, limit: int = 10) -> List[PromptCard]:
        """인기 프롬프트 조회 (조회수 기준)"""
        published_prompts = self.get_published_prompts()
        return sorted(published_prompts, key=lambda p: p.views, reverse=True)[:limit]
    
    def get_trending_prompts(self, limit: int = 10) -> List[PromptCard]:
        """트렌딩 프롬프트 조회 (좋아요 기준)"""
        published_prompts = self.get_published_prompts()
        return sorted(published_prompts, key=lambda p: p.likes, reverse=True)[:limit]
    
    def get_recent_prompts(self, limit: int = 10) -> List[PromptCard]:
        """최신 프롬프트 조회"""
        published_prompts = self.get_published_prompts()
        return sorted(published_prompts, key=lambda p: p.created_at, reverse=True)[:limit]
    
    def search_prompts(self, query: str) -> List[PromptCard]:
        """프롬프트 검색 (제목, 설명, 태그에서 검색)"""
        all_prompts = self.get_published_prompts()
        query_lower = query.lower()
        
        results = []
        for prompt in all_prompts:
            # 제목에서 검색
            if query_lower in prompt.title.lower():
                results.append(prompt)
                continue
            
            # 설명에서 검색
            if query_lower in prompt.description.lower():
                results.append(prompt)
                continue
            
            # 태그에서 검색
            if any(query_lower in tag.lower() for tag in prompt.tags):
                results.append(prompt)
                continue
        
        return results
    
    def increment_views(self, prompt_id: str) -> bool:
        """조회수 증가"""
        prompt = self.find_by_id(prompt_id, "prompt_id")
        if prompt:
            prompt.views += 1
            prompt.updated_at = datetime.now()
            return self.update(prompt, "prompt_id")
        return False
    
    def increment_likes(self, prompt_id: str) -> bool:
        """좋아요 수 증가"""
        prompt = self.find_by_id(prompt_id, "prompt_id")
        if prompt:
            prompt.likes += 1
            prompt.updated_at = datetime.now()
            return self.update(prompt, "prompt_id")
        return False
    
    def decrement_likes(self, prompt_id: str) -> bool:
        """좋아요 수 감소"""
        prompt = self.find_by_id(prompt_id, "prompt_id")
        if prompt:
            prompt.likes = max(0, prompt.likes - 1)
            prompt.updated_at = datetime.now()
            return self.update(prompt, "prompt_id")
        return False
    
    def increment_bookmarks(self, prompt_id: str) -> bool:
        """북마크 수 증가"""
        prompt = self.find_by_id(prompt_id, "prompt_id")
        if prompt:
            prompt.bookmarks += 1
            prompt.updated_at = datetime.now()
            return self.update(prompt, "prompt_id")
        return False
    
    def increment_shares(self, prompt_id: str) -> bool:
        """공유 수 증가"""
        prompt = self.find_by_id(prompt_id, "prompt_id")
        if prompt:
            prompt.shares += 1
            prompt.updated_at = datetime.now()
            return self.update(prompt, "prompt_id")
        return False
    
    def update_tier(self, prompt_id: str, new_tier: str) -> bool:
        """프롬프트 등급 업데이트 (basic, premium, featured)"""
        if new_tier not in ["basic", "premium", "featured"]:
            return False
            
        prompt = self.find_by_id(prompt_id, "prompt_id")
        if prompt:
            prompt.tier = new_tier
            prompt.updated_at = datetime.now()
            return self.update(prompt, "prompt_id")
        return False
    
    def get_prompts_with_pagination(self, page: int = 1, per_page: int = 12) -> dict:
        """페이지네이션이 적용된 프롬프트 조회"""
        all_prompts = self.get_published_prompts()
        total = len(all_prompts)
        
        start = (page - 1) * per_page
        end = start + per_page
        
        prompts = sorted(all_prompts, key=lambda p: p.created_at, reverse=True)[start:end]
        
        return {
            "prompts": prompts,
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": (total + per_page - 1) // per_page,
            "has_next": end < total,
            "has_prev": page > 1
        }