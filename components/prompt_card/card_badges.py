"""
프롬프트 카드 뱃지 컴포넌트
"""
import flet as ft
from flet import Colors
from typing import List
from config.app_config import config


def create_ai_badge(ai_model_key: str) -> ft.Container:
    """AI 모델 뱃지"""
    ai_config = config.get_ai_model_config(ai_model_key)
    
    return ft.Container(
        content=ft.Text(
            ai_config["label"], 
            size=10, 
            weight=ft.FontWeight.BOLD, 
            color=ai_config["text_color"]
        ),
        bgcolor=ai_config["color"],
        border_radius=12,
        padding=ft.padding.symmetric(horizontal=8, vertical=4),
    )


def create_category_badge(category: str) -> ft.Container:
    """카테고리 뱃지"""
    category_config = config.get_category_config(category)
    
    return ft.Container(
        content=ft.Text(
            category, 
            size=10, 
            weight=ft.FontWeight.BOLD, 
            color=category_config["text_color"]
        ),
        bgcolor=category_config["color"],
        border_radius=12,
        padding=ft.padding.symmetric(horizontal=8, vertical=4),
    )


def create_tags_row(tags_str: str) -> ft.Row:
    """태그 행 생성"""
    if not tags_str or not tags_str.strip():
        return ft.Row([])
    
    tags = [t.strip() for t in tags_str.split(",") if t.strip()]
    tag_controls = []
    
    max_display = config.business.MAX_TAGS_DISPLAY
    
    for tag in tags[:max_display]:
        tag_controls.append(
            ft.Container(
                content=ft.Text(f"#{tag}", size=10, color=Colors.GREY_700),
                bgcolor=Colors.GREY_100,
                border_radius=8,
                padding=ft.padding.symmetric(horizontal=6, vertical=2),
            )
        )
    
    if len(tags) > max_display:
        tag_controls.append(
            ft.Container(
                content=ft.Text(f"+{len(tags)-max_display}", size=10, color=Colors.GREY_600),
                bgcolor=Colors.GREY_50,
                border_radius=8,
                padding=ft.padding.symmetric(horizontal=6, vertical=2),
            )
        )
    
    return ft.Row(tag_controls, tight=True)
