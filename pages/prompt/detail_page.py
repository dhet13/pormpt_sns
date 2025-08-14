import flet as ft
from flet import Colors
from typing import Dict

from components.header import create_header
from services.prompt_service import get_prompt_by_id
from services.interactions_service import record_view, toggle_like, toggle_bookmark
from services.comment_service import get_comments_by_prompt, add_comment, toggle_comment_like, organize_comments_tree
from services.auth_service import get_current_user
from components.toast import show_toast
from models.comment import Comment




def build_prompt_detail_view(page: ft.Page, prompt_id: str) -> ft.View:
    header = create_header(page)

    # 현재 사용자 정보
    current_user = get_current_user(page)
    user_id = current_user.get("user_id") if current_user else ""
    username = current_user.get("username") if current_user else ""

    # 조회수 증가: 상세 페이지 진입 시 기록 + 디버그 출력
    try:
        new_views = record_view(user_id, prompt_id)
        print(f"[DEBUG] detail enter: id={prompt_id}, views={new_views}")
    except Exception as ex:
        print(f"[DEBUG] record_view error: {ex}")

    # 갱신된 데이터 재조회
    prompt = get_prompt_by_id(prompt_id) or {}
    if not prompt:
        return ft.View(route=f"/prompt/{prompt_id}", controls=[header, ft.Container(content=ft.Text("프롬프트를 찾을 수 없습니다."), padding=20)])

    # 댓글 데이터 로드
    comments = get_comments_by_prompt(prompt_id)
    comment_tree = organize_comments_tree(comments)

    # 좋아요/북마크 상태 (간단 구현)
    likes_count = int(prompt.get("likes", 0))
    bookmarks_count = int(prompt.get("bookmarks", 0))

    def handle_like(e):
        if not current_user:
            show_toast(page, "로그인이 필요합니다.", 3000)
            return
        try:
            new_count = toggle_like(user_id, prompt_id)
            likes_text.value = f"❤️ {new_count}"
            likes_text.update()
            show_toast(page, "좋아요가 반영되었습니다.", 2000)
        except Exception as ex:
            print(f"[DEBUG] like error: {ex}")
            show_toast(page, "오류가 발생했습니다.", 2000)

    def handle_bookmark(e):
        if not current_user:
            show_toast(page, "로그인이 필요합니다.", 3000)
            return
        try:
            new_count = toggle_bookmark(user_id, prompt_id)
            bookmark_text.value = f"🔖 {new_count}"
            bookmark_text.update()
            show_toast(page, "북마크가 반영되었습니다.", 2000)
        except Exception as ex:
            print(f"[DEBUG] bookmark error: {ex}")
            show_toast(page, "오류가 발생했습니다.", 2000)

    # 댓글 작성
    comment_input = ft.TextField(
        hint_text="댓글을 입력하세요...",
        multiline=True,
        min_lines=2,
        max_lines=4,
        border=ft.InputBorder.OUTLINE,
        width=600
    )

    def refresh_comments():
        """댓글 목록을 다시 로드하여 UI 업데이트"""
        try:
            print(f"[DEBUG] refresh_comments 시작")
            
            # 새로운 댓글 목록 로드
            fresh_comments = get_comments_by_prompt(prompt_id)
            fresh_tree = organize_comments_tree(fresh_comments)
            print(f"[DEBUG] 새로운 댓글 로드 완료: {len(fresh_comments)}개")
            
            # 댓글 수 업데이트
            comments_count_text.value = f"💬 {len(fresh_comments)}"
            comments_count_text.update()
            print(f"[DEBUG] 댓글 수 텍스트 업데이트: {len(fresh_comments)}개")
            
            # 기존 댓글 목록 완전 제거 (인덱스 5부터)
            comment_list_start = 5
            original_length = len(comments_section.controls)
            while len(comments_section.controls) > comment_list_start:
                comments_section.controls.pop()
            
            print(f"[DEBUG] 댓글 UI 정리: {original_length} -> {len(comments_section.controls)}")
            
            # 새 댓글 UI 생성 및 추가
            if fresh_comments:
                for comment in fresh_tree["root_comments"]:
                    comment_ui = _create_comment_ui(comment, fresh_tree["replies_by_parent"], current_user, prompt_id, page, refresh_comments)
                    comments_section.controls.append(comment_ui)
                    comments_section.controls.append(ft.Container(height=8))
                    print(f"[DEBUG] 댓글 UI 추가: {comment.content[:30]}...")
            else:
                comments_section.controls.append(ft.Text("아직 댓글이 없습니다.", size=14, color=Colors.GREY_500))
                print(f"[DEBUG] '댓글 없음' 메시지 추가")
            
            # UI 업데이트
            comments_section.update()
            print(f"[DEBUG] 댓글 섹션 업데이트 완료: 총 {len(comments_section.controls)}개 컨트롤")
            
        except Exception as ex:
            print(f"[DEBUG] 댓글 새로고침 오류: {ex}")
            import traceback
            traceback.print_exc()

    def submit_comment(e):
        if not current_user:
            show_toast(page, "로그인이 필요합니다.", 3000)
            return
        
        content = comment_input.value.strip()
        if not content:
            show_toast(page, "댓글 내용을 입력해주세요.", 2000)
            return
        
        try:
            print(f"[DEBUG] 댓글 등록 시도: prompt_id={prompt_id}, user_id={user_id}, username={username}")
            print(f"[DEBUG] 댓글 내용: '{content}'")
            
            new_comment = add_comment(prompt_id, user_id, username, content)
            print(f"[DEBUG] add_comment 반환값: {new_comment}")
            
            # 저장 후 바로 조회해서 확인
            fresh_comments = get_comments_by_prompt(prompt_id)
            print(f"[DEBUG] 저장 후 댓글 조회 결과: {len(fresh_comments)}개")
            for i, c in enumerate(fresh_comments[-3:]):  # 최근 3개만
                print(f"[DEBUG] 댓글 {i}: {c.content[:50]}...")
            
            comment_input.value = ""
            comment_input.update()
            print(f"[DEBUG] 댓글 등록 성공: {new_comment.comment_id}")
            show_toast(page, "댓글이 등록되었습니다.", 2000)
            
            # 댓글 섹션만 동적 업데이트 (페이지 새로고침 X)
            print(f"[DEBUG] 댓글 섹션 업데이트 시작")
            refresh_comments()
            
        except Exception as ex:
            print(f"[DEBUG] comment add error: {ex}")
            import traceback
            traceback.print_exc()
            show_toast(page, "댓글 등록 중 오류가 발생했습니다.", 2000)

    # UI 요소들
    likes_text = ft.Text(f"❤️ {likes_count}", size=14)
    bookmark_text = ft.Text(f"🔖 {bookmarks_count}", size=14)
    comments_count_text = ft.Text(f"💬 {len(comments)}", size=14, color=Colors.GREY_600)



    # 프롬프트 내용 부분
    prompt_content = ft.Column([
        ft.Text(prompt.get("title", "제목 없음"), size=24, weight=ft.FontWeight.BOLD),
        ft.Container(height=8),
        ft.Row([
            ft.Text(f"👤 {prompt.get('username', '익명')}", size=14, color=Colors.GREY_600),
            ft.Container(width=12),
            
            ft.Text(f"📂 {prompt.get('category', '텍스트')}", size=14, color=Colors.GREY_600),
            ft.Container(width=12),
            ft.Text(f"🤖 {prompt.get('ai_model_key', 'gpt4')}", size=14, color=Colors.GREY_600),
            ft.Container(expand=True),
            ft.Text(f"👁️ {prompt.get('views','0')}", size=14, color=Colors.GREY_700),
        ], tight=True),
        ft.Container(height=16),
        ft.Container(
            content=ft.Text(prompt.get("content", "내용이 없습니다."), size=16),
            bgcolor=Colors.GREY_50,
            border_radius=8,
            padding=16,
            border=ft.border.all(1, Colors.GREY_200)
        ),
        ft.Container(height=16),
        
        # 좋아요/북마크 버튼
        ft.Row([
            ft.ElevatedButton(
                content=ft.Row([likes_text], tight=True),
                bgcolor=Colors.RED_50,
                color=Colors.RED_600,
                on_click=handle_like
            ),
            ft.Container(width=8),
            ft.ElevatedButton(
                content=ft.Row([bookmark_text], tight=True),
                bgcolor=Colors.BLUE_50,
                color=Colors.BLUE_600,
                on_click=handle_bookmark
            ),
            ft.Container(width=8),
            comments_count_text,
        ], tight=True),
    ])

    # 댓글 섹션
    comments_section = ft.Column([
        ft.Container(height=24),
        ft.Text("💬 댓글", size=18, weight=ft.FontWeight.BOLD),
        ft.Container(height=12),
        
        # 댓글 작성 영역
        ft.Row([
            comment_input,
            ft.ElevatedButton(
                "등록",
                bgcolor=Colors.BLUE_400,
                color=Colors.WHITE,
                on_click=submit_comment
            )
        ], tight=True),
        ft.Container(height=16),
    ])

    # 댓글 목록 생성
    comment_controls = []
    for comment in comment_tree["root_comments"]:
        comment_controls.append(_create_comment_ui(comment, comment_tree["replies_by_parent"], current_user, prompt_id, page, refresh_comments))
        comment_controls.append(ft.Container(height=8))

    if comment_controls:
        comments_section.controls.extend(comment_controls)
    else:
        comments_section.controls.append(ft.Text("아직 댓글이 없습니다.", size=14, color=Colors.GREY_500))

    # 전체 본문
    body = ft.Column([
        prompt_content,
        ft.Divider(height=1, color=Colors.GREY_300),
        comments_section
    ])

    return ft.View(
        route=f"/prompt/{prompt_id}", 
        controls=[
            header, 
            ft.Container(
                content=ft.Column([body], scroll=ft.ScrollMode.AUTO), 
                padding=20,
                expand=True
            )
        ]
    )


def _create_comment_ui(comment: Comment, replies_by_parent: Dict, current_user: dict, prompt_id: str, page: ft.Page, refresh_comments_func=None) -> ft.Container:
    """댓글 UI 생성"""
    user_id = current_user.get("user_id") if current_user else ""
    
    def handle_comment_like(e):
        if not current_user:
            show_toast(page, "로그인이 필요합니다.", 3000)
            return
        try:
            new_count = toggle_comment_like(comment.comment_id, user_id)
            comment_like_text.value = f"❤️ {new_count}"
            comment_like_text.update()
        except Exception as ex:
            print(f"[DEBUG] comment like error: {ex}")

    def handle_reply(e):
        if not current_user:
            show_toast(page, "로그인이 필요합니다.", 3000)
            return
        # 대댓글 입력창 토글
        if reply_input.visible:
            reply_input.visible = False
        else:
            reply_input.visible = True
        reply_input.update()

    def submit_reply(e):
        content = reply_field.value.strip()
        if not content:
            show_toast(page, "대댓글 내용을 입력해주세요.", 2000)
            return
        
        try:
            print(f"[DEBUG] 대댓글 등록 시도: parent_id={comment.comment_id}, content='{content}'")
            new_reply = add_comment(prompt_id, user_id, current_user.get("username", ""), content, comment.comment_id)
            print(f"[DEBUG] 대댓글 등록 성공: {new_reply.comment_id}")
            
            reply_field.value = ""
            reply_input.visible = False
            reply_input.update()
            show_toast(page, "대댓글이 등록되었습니다.", 2000)
            
            # 댓글 섹션 업데이트 (refresh_comments 함수 사용)
            print(f"[DEBUG] 대댓글 후 댓글 섹션 업데이트")
            if refresh_comments_func:
                refresh_comments_func()
            else:
                # 폴백: 페이지 새로고침
                print(f"[DEBUG] refresh_comments_func 없음, 페이지 새로고침")
                page.go(f"/prompt/{prompt_id}")
            
        except Exception as ex:
            print(f"[DEBUG] reply add error: {ex}")
            import traceback
            traceback.print_exc()
            show_toast(page, "대댓글 등록 중 오류가 발생했습니다.", 2000)

    comment_like_text = ft.Text(f"❤️ {comment.likes}", size=12)
    
    # 대댓글 입력창
    reply_field = ft.TextField(
        hint_text="대댓글을 입력하세요...",
        multiline=True,
        min_lines=1,
        max_lines=3,
        border=ft.InputBorder.OUTLINE,
        width=500
    )
    
    reply_input = ft.Container(
        content=ft.Row([
            reply_field,
            ft.ElevatedButton("등록", bgcolor=Colors.BLUE_400, color=Colors.WHITE, on_click=submit_reply)
        ], tight=True),
        visible=False,
        margin=ft.margin.only(top=8, left=20)
    )

    # 댓글 본문
    comment_body = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text(f"👤 {comment.username}", size=12, weight=ft.FontWeight.BOLD, color=Colors.BLUE_600),
                ft.Container(expand=True),
                ft.Text(_format_time(comment.created_at), size=10, color=Colors.GREY_500),
            ], tight=True),
            ft.Container(height=4),
            ft.Text(comment.content, size=14),
            ft.Container(height=8),
            ft.Row([
                ft.TextButton(
                    content=comment_like_text,
                    on_click=handle_comment_like
                ),
                ft.TextButton("💬 답글", on_click=handle_reply),
            ], tight=True),
            reply_input,
        ]),
        bgcolor=Colors.GREY_50,
        border_radius=8,
        padding=12,
        border=ft.border.all(1, Colors.GREY_200)
    )

    # 대댓글들 추가
    reply_controls = []
    replies = replies_by_parent.get(comment.comment_id, [])
    for reply in replies:
        reply_ui = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text(f"👤 {reply.username}", size=11, weight=ft.FontWeight.BOLD, color=Colors.GREEN_600),
                    ft.Container(expand=True),
                    ft.Text(_format_time(reply.created_at), size=9, color=Colors.GREY_500),
                ], tight=True),
                ft.Container(height=2),
                ft.Text(reply.content, size=13),
                ft.Container(height=4),
                ft.Row([
                    ft.Text(f"❤️ {reply.likes}", size=11, color=Colors.GREY_600),
                ], tight=True),
            ]),
            bgcolor=Colors.GREEN_50,
            border_radius=6,
            padding=10,
            border=ft.border.all(1, Colors.GREEN_200),
            margin=ft.margin.only(left=20, top=4)
        )
        reply_controls.append(reply_ui)

    # 댓글 + 대댓글들을 포함한 전체 컨테이너
    return ft.Column([
        comment_body,
        *reply_controls
    ])


def _format_time(timestamp: float) -> str:
    """타임스탬프를 읽기 쉬운 형태로 변환"""
    try:
        import datetime
        dt = datetime.datetime.fromtimestamp(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return "방금 전"


