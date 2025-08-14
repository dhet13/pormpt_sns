import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from .csv_utils import read_csv_rows
from .user_service import update_user_points
from config.constants import FREE_VIEWS_PER_DAY, VIEW_COST


INTERACTIONS_CSV_PATH = Path("data/interactions.csv")

# 라이트 버전 설정은 config/constants.py에서 관리


def _today_str(ts: Optional[int] = None) -> str:
    dt = datetime.fromtimestamp(ts or time.time())
    return dt.strftime("%Y-%m-%d")


def _count_views_today(user_id: str) -> int:
    rows = read_csv_rows(INTERACTIONS_CSV_PATH)
    if not rows:
        return 0
    today = _today_str()
    cnt = 0
    for r in rows:
        if r.get("type") != "view":
            continue
        if r.get("user_id") != user_id:
            continue
        try:
            created_at = int(r.get("created_at") or 0)
        except Exception:
            created_at = 0
        if _today_str(created_at) == today:
            cnt += 1
    return cnt


def try_consume_view(user_id: str) -> Dict[str, object]:
    """조회 시 무료/유료 소비 처리.
    반환: {ok: bool, used_free: bool, charged: bool, remaining_points: int | None, msg: str}
    """
    if not user_id:
        return {"ok": True, "used_free": True, "charged": False, "remaining_points": None, "msg": "게스트 허용"}

    views_today = _count_views_today(user_id)
    if views_today < FREE_VIEWS_PER_DAY:
        return {"ok": True, "used_free": True, "charged": False, "remaining_points": None, "msg": "일일 무료 조회"}

    # 유료 차감 단계
    new_points = update_user_points(user_id, -VIEW_COST)
    if new_points is None:
        return {"ok": False, "used_free": False, "charged": False, "remaining_points": None, "msg": "포인트 부족"}
    return {"ok": True, "used_free": False, "charged": True, "remaining_points": new_points, "msg": "포인트 차감"}


