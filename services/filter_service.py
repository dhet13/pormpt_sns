"""
필터링 서비스
"""
from pathlib import Path
from typing import List, Dict, Any, Optional
from .csv_utils import read_csv_rows


def filter_prompts_by_category(category: str) -> List[Dict[str, Any]]:
    """카테고리별 프롬프트 필터링"""
    try:
        prompts_data = read_csv_rows(Path("data/prompts.csv"))
        if not prompts_data:
            return []
        
        if category == "전체":
            return prompts_data
        
        results = []
        for prompt in prompts_data:
            prompt_category = prompt.get("category", "").strip()
            if prompt_category == category:
                results.append(prompt)
        
        # 최신순으로 정렬
        results.sort(key=lambda x: _safe_sort_key(x), reverse=True)
        
        print(f"[DEBUG] 카테고리 '{category}' 필터링: {len(results)}개 결과")
        return results
        
    except Exception as e:
        print(f"[ERROR] 카테고리 필터링 오류: {e}")
        return []


def filter_prompts_by_ai_model(ai_model_key: str) -> List[Dict[str, Any]]:
    """AI 모델별 프롬프트 필터링"""
    try:
        prompts_data = read_csv_rows(Path("data/prompts.csv"))
        if not prompts_data:
            return []
        
        if ai_model_key == "전체":
            return prompts_data
        
        results = []
        for prompt in prompts_data:
            prompt_ai_model = prompt.get("ai_model_key", "").strip()
            if prompt_ai_model == ai_model_key:
                results.append(prompt)
        
        # 최신순으로 정렬
        results.sort(key=lambda x: _safe_sort_key(x), reverse=True)
        
        print(f"[DEBUG] AI 모델 '{ai_model_key}' 필터링: {len(results)}개 결과")
        return results
        
    except Exception as e:
        print(f"[ERROR] AI 모델 필터링 오류: {e}")
        return []


def get_available_categories() -> List[str]:
    """사용 가능한 카테고리 목록 반환"""
    try:
        prompts_data = read_csv_rows(Path("data/prompts.csv"))
        if not prompts_data:
            return ["전체"]
        
        categories = set()
        for prompt in prompts_data:
            category = prompt.get("category", "").strip()
            if category:
                categories.add(category)
        
        result = ["전체"] + sorted(list(categories))
        return result
        
    except Exception as e:
        print(f"[ERROR] 카테고리 목록 조회 오류: {e}")
        return ["전체"]


def get_available_ai_models() -> List[Dict[str, str]]:
    """사용 가능한 AI 모델 목록 반환"""
    try:
        prompts_data = read_csv_rows(Path("data/prompts.csv"))
        if not prompts_data:
            return [{"key": "전체", "name": "전체"}]
        
        ai_models = set()
        for prompt in prompts_data:
            ai_model_key = prompt.get("ai_model_key", "").strip()
            if ai_model_key:
                ai_models.add(ai_model_key)
        
        # AI 모델 키를 이름으로 변환
        model_mapping = {
            "gpt4": "ChatGPT",
            "claude": "Claude", 
            "midjourney": "Midjourney",
            "gemini": "Gemini",
            "stable_diffusion": "Stable Diffusion"
        }
        
        result = [{"key": "전체", "name": "전체"}]
        for key in sorted(ai_models):
            name = model_mapping.get(key, key.title())
            result.append({"key": key, "name": name})
        
        return result
        
    except Exception as e:
        print(f"[ERROR] AI 모델 목록 조회 오류: {e}")
        return [{"key": "전체", "name": "전체"}]


def _safe_sort_key(x):
    """안전한 정렬 키 생성"""
    created_at = x.get("created_at", "0")
    if not created_at or created_at.strip() == "":
        return 0
    try:
        return int(created_at)
    except ValueError:
        return 0
