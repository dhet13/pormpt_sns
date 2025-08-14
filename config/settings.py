import os
from pathlib import Path

#프로젝트 루트 디렉토리
BASE_DIR = Path(__file__).parent.parent

#데이터 디렉토리
DATA_DIR = BASE_DIR / "data"

#앱 설정
APP_SETTINGS = {
    "title": "Promptub",
    "version": "0.1.0",
    "description": "AI 프롬프트 공유 SNS",
    "window_width": 1200,
    "window_height": 800,
    "window_resizable": True,
    "theme_mode": "light"
}

#CSV 파일 경로
CSV_FILES = {
   "users": DATA_DIR / "users.csv",
   "prompts": DATA_DIR / "prompts.csv",
   "comments": DATA_DIR / "comments.csv",
   "likes": DATA_DIR / "likes.csv",
   "tags": DATA_DIR / "tags.csv",
   "categories": DATA_DIR / "categories.csv",
   "settings": DATA_DIR / "settings.csv",
   "notifications": DATA_DIR / "notifications.csv",
   "messages": DATA_DIR / "messages.csv",
   "interactions": DATA_DIR / "interactions.csv",
}

#페이지 설정
PAGINATION = {
    "prompts_per_page": 10,
    "comments_per_page": 10,
    "users_per_page": 10,
    "tags_per_page": 10,
    "categories_per_page": 10,
    "notifications_per_page": 10,
    "messages_per_page": 10,
}
