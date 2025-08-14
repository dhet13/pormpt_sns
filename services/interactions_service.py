import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .csv_utils import read_csv_rows, write_csv_rows
from .prompt_service import PROMPTS_CSV_PATH, increment_prompt_stat


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
INTERACTIONS_CSV_PATH = DATA_DIR / "interactions.csv"


def _ensure_interactions_file() -> None:
    if not INTERACTIONS_CSV_PATH.exists():
        INTERACTIONS_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
        write_csv_rows(
            INTERACTIONS_CSV_PATH,
            [],
            ["interaction_id", "user_id", "prompt_id", "type", "created_at"],
        )


def _load_interactions() -> List[Dict[str, str]]:
    _ensure_interactions_file()
    return read_csv_rows(INTERACTIONS_CSV_PATH)


def _save_interactions(rows: List[Dict[str, str]]) -> None:
    write_csv_rows(
        INTERACTIONS_CSV_PATH,
        rows,
        ["interaction_id", "user_id", "prompt_id", "type", "created_at"],
    )


def _now_ts() -> str:
    return str(int(time.time()))


def _exists_interaction(rows: List[Dict[str, str]], user_id: str, prompt_id: str, itype: str) -> Optional[int]:
    for idx, r in enumerate(rows):
        if (
            r.get("user_id") == user_id
            and r.get("prompt_id") == prompt_id
            and r.get("type") == itype
        ):
            return idx
    return None


def toggle_like(user_id: str, prompt_id: str) -> Tuple[bool, int]:
    """좋아요 토글. 반환: (현재 좋아요 상태, 총 좋아요 수)"""
    rows = _load_interactions()
    found_idx = _exists_interaction(rows, user_id, prompt_id, "like")
    if found_idx is not None:
        # 좋아요 해제
        rows.pop(found_idx)
        _save_interactions(rows)
        # 카운트 감소
        new_count = increment_prompt_stat(prompt_id, "likes", -1) or 0
        return (False, new_count)
    # 좋아요 추가
    rows.append(
        {
            "interaction_id": f"i_{user_id}_{prompt_id}_like",
            "user_id": user_id,
            "prompt_id": prompt_id,
            "type": "like",
            "created_at": _now_ts(),
        }
    )
    _save_interactions(rows)
    new_count = increment_prompt_stat(prompt_id, "likes", 1) or 0
    return (True, new_count)


def toggle_bookmark(user_id: str, prompt_id: str) -> Tuple[bool, int]:
    """북마크 토글. 반환: (현재 북마크 상태, 총 북마크 수)"""
    rows = _load_interactions()
    found_idx = _exists_interaction(rows, user_id, prompt_id, "bookmark")
    if found_idx is not None:
        rows.pop(found_idx)
        _save_interactions(rows)
        new_count = increment_prompt_stat(prompt_id, "bookmarks", -1) or 0
        return (False, new_count)
    rows.append(
        {
            "interaction_id": f"i_{user_id}_{prompt_id}_bookmark",
            "user_id": user_id,
            "prompt_id": prompt_id,
            "type": "bookmark",
            "created_at": _now_ts(),
        }
    )
    _save_interactions(rows)
    new_count = increment_prompt_stat(prompt_id, "bookmarks", 1) or 0
    return (True, new_count)


def record_view(user_id: Optional[str], prompt_id: str) -> int:
    """조회 기록 + 카운트 증가. 반환: 총 조회수"""
    rows = _load_interactions()
    rows.append(
        {
            "interaction_id": f"i_{user_id or 'guest'}_{prompt_id}_view_{_now_ts()}",
            "user_id": user_id or "",
            "prompt_id": prompt_id,
            "type": "view",
            "created_at": _now_ts(),
        }
    )
    _save_interactions(rows)
    return increment_prompt_stat(prompt_id, "views", 1) or 0


def record_share(user_id: Optional[str], prompt_id: str) -> int:
    """공유 기록 + 카운트 증가. 반환: 총 공유수"""
    rows = _load_interactions()
    rows.append(
        {
            "interaction_id": f"i_{user_id or 'guest'}_{prompt_id}_share_{_now_ts()}",
            "user_id": user_id or "",
            "prompt_id": prompt_id,
            "type": "share",
            "created_at": _now_ts(),
        }
    )
    _save_interactions(rows)
    return increment_prompt_stat(prompt_id, "shares", 1) or 0


