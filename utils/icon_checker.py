"""
Promptub 메인 애플리케이션 - 이모지 안정 버전
"""
import flet as ft
from flet import Colors
import csv
from pathlib import Path

def main(page: ft.Page):
    # 기본 페이지 설정
    page.title = "Promptub - AI 프롬프트 공유 SNS"
    page.window_width = 1200
    page.window_height = 800
    page.window_resizable = True
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 0
    
    # 헤더
    header = create_header()
    
    # 메인 컨테이너
    main_container = ft.Column([], spacing=0, expand=True)
    
    # 전체 레이아웃
    page.add(
        ft.Column([
            header,
            ft.Container(
                content=main_container,
                padding=20,
                expand=True
            )
        ], spacing=0)
    )
    
    # 프롬프트 카드들 로드
    load_prompt_cards(main_container, page)

def create_header() -> ft.Container:
    """헤더 컴포넌트"""
    return ft.Container(
        content=ft.Row([
            # 로고
            ft.Row([
                ft.Text("🚀", size=28),
                ft.Text("Promptub", size=24, weight=ft.FontWeight.BOLD, color=Colors.BLUE_700)
            ], tight=True),
            
            # 검색바
            ft.Container(
                content=ft.Row([
                    ft.TextField(
                        hint_text="🔍 프롬프트 검색...",
                        border=ft.InputBorder.OUTLINE,
                        dense=True,
                        width=300
                    ),
                    ft.ElevatedButton(
                        "검색", 
                        bgcolor=Colors.BLUE_400, 
                        color=Colors.WHITE
                    )
                ], tight=True),
                expand=True,
                alignment=ft.alignment.center
            ),
            
            # 사용자 메뉴
            ft.Row([
                ft.ElevatedButton(
                    "✏️ 새 프롬프트",
                    bgcolor=Colors.GREEN_400,
                    color=Colors.WHITE
                ),
                ft.ElevatedButton(
                    "👤 로그인",
                    bgcolor=Colors.GREY_600,
                    color=Colors.WHITE
                )
            ])
        ]),
        bgcolor=Colors.WHITE,
        padding=20,
        border=ft.border.only(bottom=ft.BorderSide(2, Colors.GREY_200)),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=4,
            color=Colors.with_opacity(0.1, Colors.BLACK),
            offset=ft.Offset(0, 2)
        )
    )

def create_prompt_card(prompt_data: dict) -> ft.Container:
    """프롬프트 카드 생성"""
    return ft.Container(
        content=ft.Column([
            # 헤더 (제목 + AI 모델)
            ft.Row([
                ft.Container(
                    content=ft.Text(
                        prompt_data.get("title", "제목 없음"),
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        max_lines=2
                    ),
                    expand=True
                ),
                create_ai_badge(prompt_data.get("ai_model_key", "unknown"))
            ]),
            
            ft.Divider(height=1, color=Colors.GREY_300),
            
            # 설명
            ft.Text(
                prompt_data.get("content", "설명이 없습니다.")[:150] + ("..." if len(prompt_data.get("content", "")) > 150 else ""),
                size=14,
                color=Colors.GREY_700,
                max_lines=3
            ),
            
            # 태그들 (있다면)
            create_tags_row(prompt_data.get("tags", "")),
            
            ft.Container(height=10),  # 여백
            
            # 통계
            ft.Row([
                ft.Text(f"👁️ {prompt_data.get('views', '0')}", size=12, color=Colors.GREY_600),
                ft.Container(width=20),
                ft.Text(f"❤️ {prompt_data.get('likes', '0')}", size=12, color=Colors.GREY_600),
                ft.Container(width=20),
                ft.Text(f"⭐ {prompt_data.get('bookmarks', '0')}", size=12, color=Colors.GREY_600),
                ft.Container(expand=True),
                ft.Text(f"👨‍💻 {prompt_data.get('username', '익명')}", size=12, color=Colors.GREY_500)
            ]),
            
            ft.Container(height=15),  # 여백
            
            # 액션 버튼들
            ft.Row([
                ft.ElevatedButton(
                    "👀 보기 (2포인트)",
                    bgcolor=Colors.BLUE_400,
                    color=Colors.WHITE,
                    expand=True
                ),
                ft.Container(width=8),
                ft.ElevatedButton(
                    "❤️",
                    bgcolor=Colors.RED_400,
                    color=Colors.WHITE,
                    tooltip="좋아요"
                ),
                ft.ElevatedButton(
                    "⭐",
                    bgcolor=Colors.ORANGE_400,
                    color=Colors.WHITE,
                    tooltip="즐겨찾기"
                ),
                ft.ElevatedButton(
                    "📤",
                    bgcolor=Colors.GREEN_400,
                    color=Colors.WHITE,
                    tooltip="공유"
                )
            ])
        ]),
        bgcolor=Colors.WHITE,
        border=ft.border.all(1, Colors.GREY_300),
        border_radius=12,
        padding=20,
        margin=16,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=8,
            color=Colors.with_opacity(0.1, Colors.BLACK),
            offset=ft.Offset(0, 2)
        )
    )

def create_ai_badge(ai_model_key: str) -> ft.Container:
    """AI 모델 뱃지"""
    ai_info = {
        "gpt4": {"emoji": "🤖", "name": "GPT-4", "color": Colors.GREEN_400},
        "gpt35": {"emoji": "🤖", "name": "GPT-3.5", "color": Colors.GREEN_300},
        "claude": {"emoji": "🧠", "name": "Claude", "color": Colors.ORANGE_400},
        "clova_x": {"emoji": "🇰🇷", "name": "CLOVA X", "color": Colors.GREEN_600},
        "midjourney": {"emoji": "🎨", "name": "Midjourney", "color": Colors.PURPLE_400},
    }.get(ai_model_key, {"emoji": "❓", "name": "Unknown", "color": Colors.GREY_400})
    
    return ft.Container(
        content=ft.Row([
            ft.Text(ai_info["emoji"], size=14),
            ft.Text(ai_info["name"], size=10, weight=ft.FontWeight.BOLD, color=Colors.WHITE)
        ], tight=True),
        bgcolor=ai_info["color"],
        border_radius=12,
        padding=8
    )

def create_tags_row(tags_str: str) -> ft.Row:
    """태그 행 생성"""
    if not tags_str or not tags_str.strip():
        return ft.Container(height=0)
    
    tags = [tag.strip() for tag in tags_str.split(",") if tag.strip()]
    tag_widgets = []
    
    for tag in tags[:3]:  # 최대 3개만 표시
        tag_widgets.append(
            ft.Container(
                content=ft.Text(f"#{tag}", size=10, color=Colors.BLUE_700),
                bgcolor=Colors.BLUE_50,
                border=ft.border.all(1, Colors.BLUE_200),
                border_radius=8,
                padding=6,
                margin=4
            )
        )
    
    return ft.Row(tag_widgets) if tag_widgets else ft.Container(height=0)

def load_prompt_cards(container: ft.Column, page: ft.Page):
    """프롬프트 카드들 로드"""
    try:
        prompts_file = Path("data/prompts.csv")
        users_file = Path("data/users.csv")
        
        if prompts_file.exists() and users_file.exists():
            # 사용자 데이터 읽기
            users = {}
            with open(users_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for user in reader:
                    users[user['user_id']] = user['username']
            
            # 프롬프트 데이터 읽기
            with open(prompts_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                prompts = list(reader)
            
            # 제목 추가
            container.controls.append(
                ft.Row([
                    ft.Text("🔥", size=24),
                    ft.Text("인기 프롬프트", size=20, weight=ft.FontWeight.BOLD, color=Colors.GREY_800)
                ], tight=True)
            )
            container.controls.append(ft.Container(height=10))
            
            # 카드들 생성
            for prompt in prompts:
                prompt['username'] = users.get(prompt['user_id'], '익명')
                card = create_prompt_card(prompt)
                container.controls.append(card)
                
        else:
            container.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text("📭", size=64),
                        ft.Text("아직 프롬프트가 없습니다", size=16, weight=ft.FontWeight.BOLD),
                        ft.Text("첫 번째 프롬프트를 작성해보세요!", size=14, color=Colors.GREY_600)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    alignment=ft.alignment.center,
                    padding=40
                )
            )
    
    except Exception as e:
        container.controls.append(
            ft.Row([
                ft.Text("⚠️", size=16),
                ft.Text(f"오류: {str(e)}", color=Colors.RED)
            ])
        )
    
    page.update()

if __name__ == "__main__":
    ft.app(target=main, port=8000)