from dataclasses import dataclass
from typing import Optional
import time


@dataclass
class Comment:
    """댓글 데이터 모델"""
    comment_id: str
    prompt_id: str
    user_id: str
    username: str  # 표시용 사용자명
    content: str
    parent_comment_id: Optional[str] = None  # 대댓글인 경우 부모 댓글 ID
    likes: int = 0
    created_at: float = 0.0
    updated_at: float = 0.0
    status: str = "active"  # active, deleted, hidden

    def __post_init__(self):
        if self.created_at == 0.0:
            self.created_at = time.time()
        if self.updated_at == 0.0:
            self.updated_at = time.time()

    def is_reply(self) -> bool:
        """대댓글인지 확인"""
        result = bool(self.parent_comment_id)
        if result:
            print(f"[DEBUG] 대댓글 확인: comment_id={self.comment_id}, parent_id={self.parent_comment_id}")
        return result

    def to_dict(self) -> dict:
        """딕셔너리로 변환"""
        return {
            "comment_id": self.comment_id,
            "prompt_id": self.prompt_id,
            "user_id": self.user_id,
            "username": self.username,
            "content": self.content,
            "parent_comment_id": self.parent_comment_id or "",
            "likes": str(self.likes),
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Comment":
        """딕셔너리에서 생성"""
        try:
            likes = int(data.get("likes", 0))
        except (ValueError, TypeError):
            likes = 0
        
        try:
            created_at = float(data.get("created_at", 0))
        except (ValueError, TypeError):
            created_at = time.time()
        
        try:
            updated_at = float(data.get("updated_at", 0))
        except (ValueError, TypeError):
            updated_at = time.time()

        parent_id = data.get("parent_comment_id")
        if parent_id == "" or parent_id == "0":
            parent_id = None

        return cls(
            comment_id=data.get("comment_id", ""),
            prompt_id=data.get("prompt_id", ""),
            user_id=data.get("user_id", ""),
            username=data.get("username", ""),
            content=data.get("content", ""),
            parent_comment_id=parent_id,
            likes=likes,
            created_at=created_at,
            updated_at=updated_at,
            status=data.get("status", "active")
        )
