import uuid
import time
from pathlib import Path
from typing import List, Optional, Dict
from models.comment import Comment
from services.csv_utils import read_csv_rows, write_csv_rows, ensure_fields_exist


# CSV 파일 경로
CSV_PATH = Path(__file__).parent.parent / "data" / "comments.csv"

# 필요한 필드 정의
COMMENT_FIELDS = [
    "comment_id", "prompt_id", "user_id", "username", "content",
    "parent_comment_id", "likes", "created_at", "updated_at", "status"
]


def ensure_comments_schema():
    """comments.csv 파일과 스키마 확인"""
    if not CSV_PATH.exists():
        # 빈 파일 생성
        write_csv_rows(CSV_PATH, [], COMMENT_FIELDS)
    else:
        # 기존 파일의 필드 확인 및 보완
        rows = read_csv_rows(CSV_PATH)
        ensure_fields_exist(rows, COMMENT_FIELDS, COMMENT_FIELDS)
        write_csv_rows(CSV_PATH, rows, COMMENT_FIELDS)


def get_comments_by_prompt(prompt_id: str) -> List[Comment]:
    """특정 프롬프트의 댓글 목록 조회"""
    print(f"[DEBUG] 댓글 조회 시작: prompt_id={prompt_id}")
    
    ensure_comments_schema()
    
    if not CSV_PATH.exists():
        print(f"[DEBUG] 댓글 CSV 파일 없음: {CSV_PATH}")
        return []
    
    rows = read_csv_rows(CSV_PATH)
    print(f"[DEBUG] 전체 댓글 수: {len(rows)}")
    
    comments = []
    
    for row in rows:
        row_prompt_id = row.get("prompt_id", "")
        row_status = row.get("status", "active")
        print(f"[DEBUG] 댓글 체크: prompt_id={row_prompt_id}, status={row_status}, content={row.get('content', '')[:30]}...")
        
        if row_prompt_id == prompt_id and row_status == "active":
            try:
                comment = Comment.from_dict(row)
                comments.append(comment)
                print(f"[DEBUG] 댓글 추가됨: {comment.comment_id}")
            except Exception as e:
                print(f"[DEBUG] comment parse error: {e}")
                continue
    
    print(f"[DEBUG] 해당 프롬프트 댓글 수: {len(comments)}")
    
    # 생성 시간순 정렬 (최신순)
    comments.sort(key=lambda c: c.created_at, reverse=True)
    return comments


def get_comment_by_id(comment_id: str) -> Optional[Comment]:
    """댓글 ID로 댓글 조회"""
    ensure_comments_schema()
    
    rows = read_csv_rows(CSV_PATH)
    for row in rows:
        if row.get("comment_id") == comment_id:
            try:
                return Comment.from_dict(row)
            except Exception:
                continue
    return None


def add_comment(prompt_id: str, user_id: str, username: str, content: str, parent_comment_id: Optional[str] = None) -> Comment:
    """새 댓글 추가"""
    print(f"[DEBUG] 댓글 추가 시작: prompt_id={prompt_id}, user_id={user_id}, content={content[:50]}...")
    
    ensure_comments_schema()
    
    # 새 댓글 생성
    comment = Comment(
        comment_id=str(uuid.uuid4()).replace("-", ""),
        prompt_id=prompt_id,
        user_id=user_id,
        username=username,
        content=content.strip(),
        parent_comment_id=parent_comment_id
    )
    
    print(f"[DEBUG] 댓글 객체 생성: {comment.comment_id}")
    
    # CSV에 추가
    rows = read_csv_rows(CSV_PATH)
    print(f"[DEBUG] 기존 댓글 수: {len(rows)}")
    
    rows.append(comment.to_dict())
    write_csv_rows(CSV_PATH, rows, COMMENT_FIELDS)
    
    print(f"[DEBUG] CSV 저장 완료, 새 댓글 수: {len(rows)}")
    
    # 프롬프트의 댓글 수 업데이트
    _update_prompt_comments_count(prompt_id)
    print(f"[DEBUG] 댓글 카운트 업데이트 완료")
    
    return comment


def toggle_comment_like(comment_id: str, user_id: str) -> int:
    """댓글 좋아요 토글"""
    ensure_comments_schema()
    
    rows = read_csv_rows(CSV_PATH)
    for i, row in enumerate(rows):
        if row.get("comment_id") == comment_id:
            try:
                current_likes = int(row.get("likes", 0))
            except (ValueError, TypeError):
                current_likes = 0
            
            # 좋아요 토글 (단순 증가/감소, 실제로는 interactions.csv에서 중복 체크 필요)
            new_likes = current_likes + 1  # 간단 구현
            
            rows[i]["likes"] = str(new_likes)
            rows[i]["updated_at"] = str(time.time())
            
            write_csv_rows(CSV_PATH, rows, COMMENT_FIELDS)
            return new_likes
    
    return 0


def delete_comment(comment_id: str, user_id: str) -> bool:
    """댓글 삭제 (작성자만 가능)"""
    ensure_comments_schema()
    
    rows = read_csv_rows(CSV_PATH)
    for i, row in enumerate(rows):
        if row.get("comment_id") == comment_id and row.get("user_id") == user_id:
            rows[i]["status"] = "deleted"
            rows[i]["content"] = "[삭제된 댓글입니다]"
            rows[i]["updated_at"] = str(time.time())
            
            write_csv_rows(CSV_PATH, rows, COMMENT_FIELDS)
            
            # 프롬프트의 댓글 수 업데이트
            _update_prompt_comments_count(row.get("prompt_id"))
            return True
    
    return False


def _update_prompt_comments_count(prompt_id: str):
    """프롬프트의 댓글 수 업데이트"""
    from services.prompt_service import increment_prompt_stat
    
    # 활성 댓글 수 계산
    comments = get_comments_by_prompt(prompt_id)
    active_count = len([c for c in comments if c.status == "active"])
    
    # prompts.csv의 comments 필드 업데이트 (set_value 사용)
    increment_prompt_stat(prompt_id, "comments", set_value=active_count)


def organize_comments_tree(comments: List[Comment]) -> Dict:
    """댓글을 트리 구조로 정리 (부모-자식 관계)"""
    print(f"[DEBUG] organize_comments_tree 시작: {len(comments)}개 댓글")
    
    # 부모 댓글들
    root_comments = [c for c in comments if not c.is_reply()]
    print(f"[DEBUG] 루트 댓글 수: {len(root_comments)}")
    
    # 대댓글들을 부모별로 그룹화
    replies_by_parent = {}
    
    for comment in comments:
        if comment.is_reply():
            parent_id = comment.parent_comment_id
            print(f"[DEBUG] 대댓글 발견: parent_id={parent_id}, content={comment.content[:30]}...")
            if parent_id not in replies_by_parent:
                replies_by_parent[parent_id] = []
            replies_by_parent[parent_id].append(comment)
    
    print(f"[DEBUG] 대댓글 그룹: {len(replies_by_parent)}개 부모에 대댓글 있음")
    for parent_id, replies in replies_by_parent.items():
        print(f"[DEBUG] 부모 {parent_id}: {len(replies)}개 대댓글")
    
    return {
        "root_comments": root_comments,
        "replies_by_parent": replies_by_parent
    }
