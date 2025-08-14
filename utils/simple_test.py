"""
간단한 데이터 생성 테스트
"""
import os
from pathlib import Path

def create_test_data():
    """간단한 테스트 데이터 생성"""
    print("🔍 테스트 시작...")
    
    # data 폴더 생성
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    print(f"📁 data 폴더 경로: {data_dir.absolute()}")
    
    # 간단한 CSV 파일 생성
    users_csv = data_dir / "users.csv"
    with open(users_csv, 'w', encoding='utf-8') as f:
        f.write("user_id,username,email,points\n")
        f.write("user_001,테스트사용자,test@test.com,100\n")
        f.write("user_002,프롬프트마스터,master@test.com,500\n")
    
    prompts_csv = data_dir / "prompts.csv"
    with open(prompts_csv, 'w', encoding='utf-8') as f:
        f.write("prompt_id,user_id,title,content\n")
        f.write("prompt_001,user_001,테스트 프롬프트,이것은 테스트입니다\n")
        f.write("prompt_002,user_002,ChatGPT 프롬프트,당신은 도우미입니다\n")
    
    print(f"✅ users.csv 생성됨")
    print(f"✅ prompts.csv 생성됨")
    print("🎉 테스트 완료!")

if __name__ == "__main__":
    create_test_data()