import csv
import hashlib
import secrets
import time
from pathlib import Path
from typing import Dict, List, Optional

from .csv_utils import read_csv_rows, write_csv_rows
from .user_service import ensure_users_schema


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
USERS_CSV_PATH = DATA_DIR / "users.csv"


def _hash_password(password: str, salt: Optional[str] = None) -> Dict[str, str]:
    if salt is None:
        salt = secrets.token_hex(16)
    dk = hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=bytes.fromhex(salt),
        iterations=120_000,
        dklen=32,
    )
    return {"hash": dk.hex(), "salt": salt}


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


def _load_users() -> List[Dict[str, str]]:
    _ensure_users_file()
    return read_csv_rows(USERS_CSV_PATH)


def _save_users(rows: List[Dict[str, str]]) -> None:
    _ensure_users_file()
    write_csv_rows(
        USERS_CSV_PATH,
        rows,
        [
            "user_id",
            "username",
            "password_hash",
            "salt",
            "created_at",
            "points",
            "level",
        ],
    )


def find_user_by_username(username: str) -> Optional[Dict[str, str]]:
    username = (username or "").strip()
    if not username:
        return None
    for u in _load_users():
        if u.get("username", "").strip().lower() == username.lower():
            return u
    return None


def register_user(username: str, password: str) -> Dict[str, str]:
    ensure_users_schema()
    username = (username or "").strip()
    password = (password or "").strip()
    if len(username) < 3:
        return {"ok": False, "msg": "아이디는 3자 이상이어야 합니다."}
    if len(password) < 6:
        return {"ok": False, "msg": "비밀번호는 6자 이상이어야 합니다."}
    if find_user_by_username(username):
        return {"ok": False, "msg": "이미 존재하는 아이디입니다."}

    try:
        hp = _hash_password(password)
        user_row = {
            "user_id": secrets.token_hex(12),
            "username": username,
            "password_hash": hp["hash"],
            "salt": hp["salt"],
            "created_at": str(int(time.time())),
            "points": "100",
            "level": "1",
        }
        users = _load_users()
        users.append(user_row)
        _save_users(users)
        return {"ok": True, "msg": "회원가입이 완료되었습니다."}
    except Exception as ex:
        return {"ok": False, "msg": f"회원가입 중 오류: {ex} (경로: {USERS_CSV_PATH})"}


def authenticate_user(username: str, password: str) -> Dict[str, str]:
    ensure_users_schema()
    u = find_user_by_username(username)
    if not u:
        return {"ok": False, "msg": "존재하지 않는 아이디입니다."}
    hp = _hash_password(password, u.get("salt"))
    if hp["hash"] != (u.get("password_hash") or ""):
        return {"ok": False, "msg": "비밀번호가 일치하지 않습니다."}
    return {"ok": True, "msg": "로그인 완료", "user": {"user_id": u["user_id"], "username": u["username"]}}


def get_current_user(page) -> Optional[Dict[str, str]]:
    """현재 로그인된 사용자 정보 반환"""
    try:
        user = page.session.get("user")
        if isinstance(user, dict) and user.get("user_id"):
            return user
    except Exception:
        pass
    return None

