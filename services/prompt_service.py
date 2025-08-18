from pathlib import Path
from typing import Dict, List, Optional

from .csv_utils import read_csv_rows, write_csv_rows, ensure_fields_exist, safe_int


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PROMPTS_CSV_PATH = DATA_DIR / "prompts.csv"


def increment_prompt_stat(prompt_id: str, field: str, delta: int = 1, set_value: Optional[int] = None) -> Optional[int]:
    """프롬프트 통계 업데이트
    - delta: 증감값 (기본 1)
    - set_value: 직접 설정할 값 (delta 무시)
    """
    if not PROMPTS_CSV_PATH.exists() or not prompt_id:
        return None
    rows = read_csv_rows(PROMPTS_CSV_PATH)
    if not rows:
        return None
    fieldnames = list(rows[0].keys())
    fieldnames = ensure_fields_exist(rows, fieldnames, [field])
    updated_value: Optional[int] = None
    for r in rows:
        pid = r.get("prompt_id") or r.get("id")
        if str(pid) == str(prompt_id):
            if set_value is not None:
                # 직접 값 설정
                new_value = max(0, set_value)
            else:
                # 증감값 적용
                current = safe_int(r.get(field), 0)
                new_value = max(0, current + delta)
            r[field] = str(new_value)
            updated_value = new_value
            break
    write_csv_rows(PROMPTS_CSV_PATH, rows, fieldnames)
    return updated_value


def save_new_prompt(row: Dict[str, str]) -> None:
    rows = read_csv_rows(PROMPTS_CSV_PATH)
    fieldnames = list(rows[0].keys()) if rows else []
    base_fields = [
        "prompt_id","user_id","title","content","category","ai_model_key",
        "tags","likes","bookmarks","shares","comments","views","created_at","updated_at",
    ]
    for f in base_fields:
        if f not in fieldnames:
            fieldnames.append(f)
    rows.append(row)
    write_csv_rows(PROMPTS_CSV_PATH, rows, fieldnames)


def get_prompt_by_id(prompt_id: str) -> Optional[Dict[str, str]]:
    if not prompt_id:
        return None
    rows = read_csv_rows(PROMPTS_CSV_PATH)
    for r in rows:
        pid = r.get("prompt_id") or r.get("id")
        if str(pid) == str(prompt_id):
            return r
    return None


def update_prompt_field(prompt_id: str, field: str, value: str) -> bool:
    """프롬프트의 특정 필드 업데이트"""
    if not PROMPTS_CSV_PATH.exists() or not prompt_id:
        return False
    
    rows = read_csv_rows(PROMPTS_CSV_PATH)
    if not rows:
        return False
    
    fieldnames = list(rows[0].keys())
    fieldnames = ensure_fields_exist(rows, fieldnames, [field])
    
    updated = False
    for r in rows:
        pid = r.get("prompt_id") or r.get("id")
        if str(pid) == str(prompt_id):
            r[field] = value
            updated = True
            break
    
    if updated:
        write_csv_rows(PROMPTS_CSV_PATH, rows, fieldnames)
        print(f"[DEBUG] 프롬프트 {field} 업데이트: {prompt_id} -> {value}")
    
    return updated


def delete_prompt_by_id(prompt_id: str) -> bool:
    """프롬프트 삭제"""
    if not PROMPTS_CSV_PATH.exists() or not prompt_id:
        return False
    
    try:
        rows = read_csv_rows(PROMPTS_CSV_PATH)
        if not rows:
            return False
        
        fieldnames = list(rows[0].keys())
        original_count = len(rows)
        
        # 해당 ID의 프롬프트 제거
        rows = [r for r in rows 
                if str(r.get("prompt_id") or r.get("id") or "") != str(prompt_id)]
        
        if len(rows) < original_count:
            write_csv_rows(PROMPTS_CSV_PATH, rows, fieldnames)
            print(f"[DEBUG] 프롬프트 삭제 완료: {prompt_id}")
            return True
        else:
            print(f"[DEBUG] 삭제할 프롬프트를 찾지 못함: {prompt_id}")
            return False
            
    except Exception as e:
        print(f"[ERROR] 프롬프트 삭제 실패: {e}")
        return False


