"""
카테고리 데이터 매니저
"""
from pathlib import Path
from typing import List, Optional, Dict
from managers.base_manager import BaseManager
from models.category import Category
from config.settings import CSV_FILES

class CategoryManager(BaseManager[Category]):
    """카테고리 데이터 관리 클래스"""
    
    def __init__(self):
        super().__init__(CSV_FILES["categories"])
    
    def get_fieldnames(self) -> List[str]:
        """CSV 파일의 컬럼명 리스트 반환"""
        return [
            'category_id', 'name', 'description', 'icon', 'parent_id',
            'prompt_count', 'is_active', 'sort_order', 'created_at', 'updated_at'
        ]
    
    def dict_to_model(self, data: dict) -> Category:
        """딕셔너리를 Category 객체로 변환"""
        return Category.from_dict(data)
    
    def model_to_dict(self, model: Category) -> dict:
        """Category 객체를 딕셔너리로 변환"""
        return model.to_dict()
    
    # === 카테고리 특화 메서드들 ===
    
    def get_active_categories(self) -> List[Category]:
        """활성 카테고리만 조회"""
        return self.filter(is_active=True)
    
    def get_parent_categories(self) -> List[Category]:
        """상위 카테고리들만 조회"""
        all_categories = self.get_active_categories()
        return [cat for cat in all_categories if cat.is_parent_category()]
    
    def get_child_categories(self, parent_id: int) -> List[Category]:
        """특정 상위 카테고리의 하위 카테고리들 조회"""
        return self.filter(parent_id=parent_id, is_active=True)
    
    def get_categories_sorted(self) -> List[Category]:
        """정렬 순서대로 카테고리 조회"""
        categories = self.get_active_categories()
        return sorted(categories, key=lambda c: c.sort_order)
    
    def find_by_name(self, name: str) -> Optional[Category]:
        """이름으로 카테고리 찾기"""
        categories = self.filter(name=name)
        return categories[0] if categories else None
    
    def get_category_hierarchy(self) -> Dict[str, List[Category]]:
        """카테고리 계층 구조 반환"""
        parent_categories = self.get_parent_categories()
        hierarchy = {}
        
        for parent in sorted(parent_categories, key=lambda c: c.sort_order):
            children = self.get_child_categories(parent.category_id)
            hierarchy[parent.name] = {
                "parent": parent,
                "children": sorted(children, key=lambda c: c.sort_order)
            }
        
        return hierarchy
    
    def update_prompt_count(self, category_id: int, count_change: int = 1) -> bool:
        """카테고리의 프롬프트 수 업데이트"""
        category = self.find_by_id(str(category_id), "category_id")
        if category:
            category.prompt_count += count_change
            category.prompt_count = max(0, category.prompt_count)  # 0 이하로 떨어지지 않음
            return self.update(category, "category_id")
        return False
    
    def get_popular_categories(self, limit: int = 5) -> List[Category]:
        """인기 카테고리 조회 (프롬프트 수 기준)"""
        active_categories = self.get_active_categories()
        return sorted(active_categories, key=lambda c: c.prompt_count, reverse=True)[:limit]
    
    def search_categories(self, query: str) -> List[Category]:
        """카테고리 검색 (이름, 설명에서 검색)"""
        all_categories = self.get_active_categories()
        query_lower = query.lower()
        
        results = []
        for category in all_categories:
            if query_lower in category.name.lower() or query_lower in category.description.lower():
                results.append(category)
        
        return results
    
    def toggle_category_status(self, category_id: int) -> bool:
        """카테고리 활성/비활성 토글"""
        category = self.find_by_id(str(category_id), "category_id")
        if category:
            category.is_active = not category.is_active
            return self.update(category, "category_id")
        return False
    
    def reorder_categories(self, category_orders: Dict[int, int]) -> bool:
        """카테고리 순서 재정렬"""
        try:
            for category_id, new_order in category_orders.items():
                category = self.find_by_id(str(category_id), "category_id")
                if category:
                    category.sort_order = new_order
                    self.update(category, "category_id")
            return True
        except Exception as e:
            print(f"카테고리 순서 변경 오류: {e}")
            return False