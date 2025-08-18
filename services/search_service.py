"""
검색 서비스
"""
from pathlib import Path
from typing import List, Dict, Any
from .csv_utils import read_csv_rows


def search_prompts(query: str) -> List[Dict[str, Any]]:
    """프롬프트 검색"""
    try:
        # CSV에서 모든 프롬프트 로드
        prompts_data = read_csv_rows(Path("data/prompts.csv"))
        if not prompts_data:
            return []
        
        query_lower = query.lower().strip()
        results = []
        
        for prompt in prompts_data:
            # 제목에서 검색
            title = prompt.get("title", "").lower()
            if query_lower in title:
                results.append(prompt)
                continue
            
            # 내용에서 검색
            content = prompt.get("content", "").lower()
            if query_lower in content:
                results.append(prompt)
                continue
            
            # 태그에서 검색
            tags = prompt.get("tags", "").lower()
            if query_lower in tags:
                results.append(prompt)
                continue
            
            # 카테고리에서 검색
            category = prompt.get("category", "").lower()
            if query_lower in category:
                results.append(prompt)
                continue
        
        # 최신순으로 정렬
        def safe_sort_key(x):
            created_at = x.get("created_at", "0")
            if not created_at or created_at.strip() == "":
                return 0
            try:
                return int(created_at)
            except ValueError:
                return 0
        
        results.sort(key=safe_sort_key, reverse=True)
        
        print(f"[DEBUG] 검색어 '{query}': {len(results)}개 결과")
        return results
        
    except Exception as e:
        print(f"[ERROR] 검색 오류: {e}")
        return []


def get_search_suggestions(query: str, limit: int = 5) -> List[str]:
    """검색 제안어 생성"""
    try:
        prompts_data = read_csv_rows(Path("data/prompts.csv"))
        if not prompts_data:
            return []
        
        query_lower = query.lower().strip()
        suggestions = set()
        
        for prompt in prompts_data:
            # 제목에서 단어 추출
            title_words = prompt.get("title", "").split()
            for word in title_words:
                if len(word) >= 2 and query_lower in word.lower():
                    suggestions.add(word)
            
            # 태그에서 추출
            tags = prompt.get("tags", "").split(",")
            for tag in tags:
                tag = tag.strip()
                if len(tag) >= 2 and query_lower in tag.lower():
                    suggestions.add(tag)
        
        return list(suggestions)[:limit]
        
    except Exception as e:
        print(f"[ERROR] 검색 제안 오류: {e}")
        return []
