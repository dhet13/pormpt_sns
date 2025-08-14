"""
프롬프트 카드 UI 컴포넌트
"""
import flet as ft
from datetime import datetime

class PromptCardUI:
    """프롬프트 카드 UI 컴포넌트"""
    
    def __init__(self, prompt_data: dict):
        self.prompt_data = prompt_data
    
    def build(self) -> ft.Container:
        """프롬프트 카드 UI 생성"""
        return ft.Container(
            content=ft.Column([
                # 제목
                ft.Text(
                    self.prompt_data.get("title", "제목 없음"),
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    max_lines=2
                ),
                
                # 설명
                ft.Text(
                    self.prompt_data.get("content", "설명이 없습니다."),
                    size=14,
                    color=ft.colors.GREY_700,
                    max_lines=3
                ),
                
                # 통계
                ft.Row([
                    ft.Text(f"👀 {self.prompt_data.get('views', '0')}", size=12),
                    ft.Text(f"❤️ {self.prompt_data.get('likes', '0')}", size=12),
                    ft.Text(f"by {self.prompt_data.get('username', '익명')}", size=12)
                ]),
                
                # 버튼
                ft.ElevatedButton(
                    "보기 (2포인트)",
                    on_click=self._on_view_click
                )
            ]),
            bgcolor=ft.colors.WHITE,
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=12,
            padding=16,
            margin=8
        )
    
    def _on_view_click(self, e):
        """보기 버튼 클릭"""
        print(f"프롬프트 보기: {self.prompt_data.get('title')}")