"""
CSV 기반 데이터 매니저 기본 클래스
"""
import csv
import os
from pathlib import Path
from typing import List, Dict, Any, Optional, TypeVar, Generic
from abc import ABC, abstractmethod

T = TypeVar('T')  # 제네릭 타입 (User, PromptCard 등)

class BaseManager(ABC, Generic[T]):
    """CSV 파일 기반 데이터 매니저 기본 클래스"""
    
    def __init__(self, csv_file_path: Path):
        self.csv_file_path = csv_file_path
        self.ensure_file_exists()
    
    def ensure_file_exists(self):
        """CSV 파일이 없으면 생성"""
        if not self.csv_file_path.exists():
            # 디렉토리 생성
            self.csv_file_path.parent.mkdir(parents=True, exist_ok=True)
            # 빈 CSV 파일 생성 (헤더만)
            with open(self.csv_file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.get_fieldnames())
                writer.writeheader()
    
    @abstractmethod
    def get_fieldnames(self) -> List[str]:
        """CSV 파일의 컬럼명 리스트 반환"""
        pass
    
    @abstractmethod
    def dict_to_model(self, data: Dict[str, Any]) -> T:
        """딕셔너리를 모델 객체로 변환"""
        pass
    
    @abstractmethod
    def model_to_dict(self, model: T) -> Dict[str, Any]:
        """모델 객체를 딕셔너리로 변환"""
        pass
    
    def load_all(self) -> List[T]:
        """모든 데이터 로드"""
        try:
            with open(self.csv_file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                return [self.dict_to_model(row) for row in reader]
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"데이터 로드 오류: {e}")
            return []
    
    def save_all(self, models: List[T]):
        """모든 데이터 저장"""
        try:
            with open(self.csv_file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.get_fieldnames())
                writer.writeheader()
                for model in models:
                    writer.writerow(self.model_to_dict(model))
        except Exception as e:
            print(f"데이터 저장 오류: {e}")
    
    def find_by_id(self, id_value: str, id_field: str = 'id') -> Optional[T]:
        """ID로 데이터 찾기"""
        all_data = self.load_all()
        for item in all_data:
            if getattr(item, id_field) == id_value:
                return item
        return None
    
    def create(self, model: T) -> bool:
        """새 데이터 생성"""
        try:
            all_data = self.load_all()
            all_data.append(model)
            self.save_all(all_data)
            return True
        except Exception as e:
            print(f"데이터 생성 오류: {e}")
            return False
    
    def update(self, model: T, id_field: str = 'id') -> bool:
        """데이터 업데이트"""
        try:
            all_data = self.load_all()
            id_value = getattr(model, id_field)
            
            for i, item in enumerate(all_data):
                if getattr(item, id_field) == id_value:
                    all_data[i] = model
                    self.save_all(all_data)
                    return True
            return False  # 해당 ID 찾을 수 없음
        except Exception as e:
            print(f"데이터 업데이트 오류: {e}")
            return False
    
    def delete(self, id_value: str, id_field: str = 'id') -> bool:
        """데이터 삭제"""
        try:
            all_data = self.load_all()
            original_count = len(all_data)
            
            all_data = [item for item in all_data 
                       if getattr(item, id_field) != id_value]
            
            if len(all_data) < original_count:
                self.save_all(all_data)
                return True
            return False  # 해당 ID 찾을 수 없음
        except Exception as e:
            print(f"데이터 삭제 오류: {e}")
            return False
    
    def count(self) -> int:
        """전체 데이터 개수"""
        return len(self.load_all())
    
    def filter(self, **kwargs) -> List[T]:
        """조건에 맞는 데이터 필터링"""
        all_data = self.load_all()
        result = []
        
        for item in all_data:
            match = True
            for key, value in kwargs.items():
                if getattr(item, key, None) != value:
                    match = False
                    break
            if match:
                result.append(item)
        
        return result