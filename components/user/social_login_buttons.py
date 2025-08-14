"""
소셜 로그인 버튼 컴포넌트 (추후 구현)
"""
import flet as ft

# class SocialLoginButtons:
#     def __init__(self, page: ft.Page):
#         self.page = page
#     
#     def build(self) -> ft.Column:
#         """소셜 로그인 버튼들 생성"""
#         return ft.Column([
#             ft.Text("소셜 로그인", size=16, weight=ft.FontWeight.BOLD),
#             
#             # 구글 로그인 버튼
#             ft.ElevatedButton(
#                 content=ft.Row([
#                     ft.Text("🔍", size=16),
#                     ft.Text("Google로 계속하기")
#                 ]),
#                 bgcolor="#DB4437",
#                 color="white",
#                 on_click=self.on_google_login
#             ),
#             
#             # 카카오 로그인 버튼  
#             ft.ElevatedButton(
#                 content=ft.Row([
#                     ft.Text("💛", size=16),
#                     ft.Text("카카오로 계속하기")
#                 ]),
#                 bgcolor="#FEE500",
#                 color="black",
#                 on_click=self.on_kakao_login
#             ),
#             
#             # 네이버 로그인 버튼
#             ft.ElevatedButton(
#                 content=ft.Row([
#                     ft.Text("🟢", size=16), 
#                     ft.Text("네이버로 계속하기")
#                 ]),
#                 bgcolor="#03C75A",
#                 color="white",
#                 on_click=self.on_naver_login
#             ),
#             
#             # 깃허브 로그인 버튼
#             ft.ElevatedButton(
#                 content=ft.Row([
#                     ft.Text("🐙", size=16),
#                     ft.Text("GitHub로 계속하기") 
#                 ]),
#                 bgcolor="#333333",
#                 color="white",
#                 on_click=self.on_github_login
#             )
#         ])
#     
#     def on_google_login(self, e):
#         """구글 로그인 버튼 클릭"""
#         # 구글 OAuth 플로우 시작
#         pass
#     
#     def on_kakao_login(self, e):
#         """카카오 로그인 버튼 클릭"""
#         # 카카오 OAuth 플로우 시작
#         pass
#     
#     def on_naver_login(self, e):
#         """네이버 로그인 버튼 클릭"""
#         # 네이버 OAuth 플로우 시작
#         pass
#     
#     def on_github_login(self, e):
#         """깃허브 로그인 버튼 클릭"""
#         # 깃허브 OAuth 플로우 시작
#         pass