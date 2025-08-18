"""
프롬프트 카드 썸네일 컴포넌트
"""
import flet as ft
from flet import Colors
from typing import Dict
from config.app_config import config


def create_thumbnail_area(prompt_data: dict) -> ft.Container:
    """스마트 썸네일 시스템"""
    thumbnail_path = prompt_data.get("thumbnail_path", "")
    category = prompt_data.get("category", "텍스트")
    
    if thumbnail_path:
        return create_user_image_thumbnail(thumbnail_path)
    else:
        return create_category_thumbnail(category)


def create_user_image_thumbnail(thumbnail_path: str) -> ft.Container:
    """사용자 업로드 이미지 썸네일"""
    return ft.Container(
        content=ft.Image(src=thumbnail_path, fit=ft.ImageFit.COVER),
        width=60,
        height=60,
        border_radius=8,
        bgcolor=Colors.GREY_100,
    )


def create_category_thumbnail(category: str) -> ft.Container:
    """카테고리별 색상 + 이모지 썸네일"""
    category_config = config.get_category_config(category)
    
    return ft.Container(
        content=ft.Text(category_config["emoji"], size=24),
        width=60,
        height=60,
        bgcolor=category_config["color"],
        border_radius=8,
        alignment=ft.alignment.center,
    )
