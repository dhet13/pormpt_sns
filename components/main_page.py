import flet as ft

class MainPage:
    def __init__(self,page):
        self.page = page
    
    def build(self):
        return ft.Text("메인 페이지 작동 중")