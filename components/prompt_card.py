"""
프롬프트 카드 UI 컴포넌트 - 리팩토링된 버전
"""
# 새로운 모듈화된 컴포넌트들을 사용
from .prompt_card.card_main import create_prompt_card, load_prompt_cards

# 하위 호환성을 위한 re-export
__all__ = ['create_prompt_card', 'load_prompt_cards']