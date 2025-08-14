import csv
from pathlib import Path
from typing import List, Dict, Optional


def safe_int(value: Optional[str], default: int = 0) -> int:
    try:
        if value is None:
            return default
        return int(str(value).strip())
    except Exception:
        return default


def read_csv_rows(file_path: Path) -> List[Dict[str, str]]:
    if not file_path.exists():
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def write_csv_rows(file_path: Path, rows: List[Dict[str, str]], fieldnames: List[str]) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


def ensure_fields_exist(rows: List[Dict[str, str]], fieldnames: List[str], required_fields: List[str]) -> List[str]:
    updated_fieldnames = list(fieldnames)
    for rf in required_fields:
        if rf not in updated_fieldnames:
            updated_fieldnames.append(rf)
    for r in rows:
        for rf in required_fields:
            if rf not in r or r[rf] is None or r[rf] == "":
                r[rf] = "0"
    return updated_fieldnames


