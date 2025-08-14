import csv
from pathlib import Path
from typing import Dict, List, Optional

from .csv_utils import read_csv_rows, write_csv_rows
import csv
import time
import secrets


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
USERS_CSV_PATH = DATA_DIR / "users.csv"


def _ensure_users_file() -> None:
    if not USERS_CSV_PATH.exists():
        USERS_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(USERS_CSV_PATH, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "user_id",
                    "username",
                    "password_hash",
                    "salt",
                    "created_at",
                    "points",
                    "level",
                ],
            )
            writer.writeheader()


def ensure_users_schema() -> None:
    """users.csv 스키마를 강제합니다.
    - 기존 파일에 plaintext password가 있으면 hash+salt로 변환
    - 누락 필드는 기본값 채움
    - user_id 없으면 생성
    """
    _ensure_users_file()
    # 읽어서 필드 검사
    try:
        with open(USERS_CSV_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            existing_fields = reader.fieldnames or []
    except Exception:
        rows = []
        existing_fields = []

    desired_fields = [
        "user_id","username","password_hash","salt","created_at","points","level"
    ]

    changed = False
    new_rows = []
    now_ts = str(int(time.time()))

    for r in rows:
        new_r = {}
        # user_id
        new_r["user_id"] = r.get("user_id") or secrets.token_hex(12)
        # username
        new_r["username"] = (r.get("username") or "").strip()
        # password / password_hash
        if r.get("password_hash") and r.get("salt"):
            new_r["password_hash"] = r.get("password_hash")
            new_r["salt"] = r.get("salt")
        elif r.get("password"):
            # plaintext 비밀번호 → 해시 변환은 auth_service에서만 수행 가능하므로 빈 값으로 두고 가입/로그인 유도
            new_r["password_hash"] = ""
            new_r["salt"] = ""
            changed = True
        else:
            new_r["password_hash"] = r.get("password_hash") or ""
            new_r["salt"] = r.get("salt") or ""
        # timestamps / points / level
        new_r["created_at"] = r.get("created_at") or now_ts
        new_r["points"] = r.get("points") or "0"
        new_r["level"] = r.get("level") or "1"
        new_rows.append(new_r)

    # 기존에 빈 파일이면 변경 없이 종료
    if not rows:
        return

    # 필드 불일치 또는 변환 발생 시 덮어쓰기
    if set(existing_fields) != set(desired_fields) or changed:
        write_csv_rows(USERS_CSV_PATH, new_rows, desired_fields)


def get_user_by_id(user_id: str) -> Optional[Dict[str, str]]:
    ensure_users_schema()
    for u in read_csv_rows(USERS_CSV_PATH):
        if u.get("user_id") == user_id:
            return u
    return None


def update_user_points(user_id: str, delta: int) -> Optional[int]:
    ensure_users_schema()
    rows = read_csv_rows(USERS_CSV_PATH)
    if not rows:
        return None
    fieldnames = list(rows[0].keys())
    updated_points: Optional[int] = None
    for r in rows:
        if r.get("user_id") == user_id:
            try:
                current = int(r.get("points") or 0)
            except Exception:
                current = 0
            new_points = current + delta
            if new_points < 0:
                return None
            r["points"] = str(new_points)
            updated_points = new_points
            break
    if updated_points is None:
        return None
    write_csv_rows(USERS_CSV_PATH, rows, fieldnames)
    return updated_points


