"""
기존 사용자들에게 초기 포인트 100점 지급하는 스크립트
"""
import sys
from pathlib import Path

# 프로젝트 루트를 sys.path에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from services.csv_utils import read_csv_rows, write_csv_rows

def update_user_points():
    users_csv = project_root / "data" / "users.csv"
    
    if not users_csv.exists():
        print("users.csv 파일이 없습니다.")
        return
    
    # 사용자 데이터 로드
    rows = read_csv_rows(users_csv)
    updated_count = 0
    
    for row in rows:
        current_points = int(row.get("points", 0))
        if current_points == 0:
            row["points"] = "100"
            updated_count += 1
            print(f"사용자 {row.get('username')}에게 100점 지급")
    
    # 업데이트된 데이터 저장
    fieldnames = ["user_id", "username", "password_hash", "salt", "created_at", "points", "level"]
    write_csv_rows(users_csv, rows, fieldnames)
    
    print(f"총 {updated_count}명의 사용자에게 포인트를 지급했습니다.")

if __name__ == "__main__":
    update_user_points()
