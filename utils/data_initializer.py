"""
초기 데이터 설정
"""
from datetime import datetime
from models.category import Category
from managers.category_manager import CategoryManager
from config.constants import CATEGORIES

def initialize_categories():
    """초기 카테고리 데이터 생성"""
    category_manager = CategoryManager()
    
    # 기존 카테고리가 있는지 확인
    existing_categories = category_manager.load_all()
    if existing_categories:
        print("카테고리가 이미 존재합니다.")
        return
    
    # constants.py의 CATEGORIES 데이터를 사용해서 초기 카테고리 생성
    categories_to_create = []
    
    for cat_data in CATEGORIES:
        category = Category(
            category_id=cat_data["id"],
            name=cat_data["name"],
            description=cat_data["description"],
            icon=cat_data["icon"],
            parent_id=None,  # 일단 모두 상위 카테고리로
            prompt_count=0,
            is_active=True,
            sort_order=cat_data["id"],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        categories_to_create.append(category)
    
    # 모든 카테고리 저장
    category_manager.save_all(categories_to_create)
    print(f"{len(categories_to_create)}개의 카테고리가 생성되었습니다.")

if __name__ == "__main__":
    initialize_categories()