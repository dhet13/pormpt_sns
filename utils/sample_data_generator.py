"""
샘플 데이터 생성기
"""
import uuid
from datetime import datetime, timedelta
import random
from models.user import User
from models.prompt_card import PromptCard
from managers.user_manager import UserManager
from managers.prompt_manager import PromptManager

def generate_sample_users():
    """샘플 사용자 데이터 생성"""
    sample_users = [
        {
            "username": "프롬프트마스터",
            "email": "master@promptub.com",
            "bio": "AI 프롬프트 전문가입니다. ChatGPT와 Claude를 주로 사용합니다.",
            "points": 1250,
            "level": 500
        },
        {
            "username": "AI크리에이터",
            "email": "creator@promptub.com", 
            "bio": "창작 프롬프트를 만드는 것을 좋아합니다.",
            "points": 850,
            "level": 100
        },
        {
            "username": "개발자김씨",
            "email": "dev@promptub.com",
            "bio": "코딩 관련 프롬프트를 주로 작성합니다.",
            "points": 650,
            "level": 100
        },
        {
            "username": "글쓰기달인",
            "email": "writer@promptub.com",
            "bio": "블로그와 콘텐츠 작성용 프롬프트 전문",
            "points": 420,
            "level": 1
        },
        {
            "username": "신입회원",
            "email": "newbie@promptub.com",
            "bio": "안녕하세요! 프롬프트 공부 중입니다.",
            "points": 50,
            "level": 1
        }
    ]
    
    users = []
    for i, user_data in enumerate(sample_users):
        user = User(
            user_id=f"user_{str(uuid.uuid4())[:8]}",
            username=user_data["username"],
            email=user_data["email"],
            password_hash="hashed_password_123",  # 실제로는 해시된 비밀번호
            bio=user_data["bio"],
            points=user_data["points"],
            level=user_data["level"],
            total_prompts=random.randint(0, 15),
            total_likes_received=random.randint(0, 50),
            follower_count=random.randint(0, 30),
            following_count=random.randint(0, 20),
            daily_free_views_used=random.randint(0, 5),
            login_streak=random.randint(1, 30),
            created_at=datetime.now() - timedelta(days=random.randint(1, 100)),
            updated_at=datetime.now(),
            status="active"
        )
        users.append(user)
    
    return users

def generate_sample_prompts(users):
    """샘플 프롬프트 데이터 생성"""
    sample_prompts = [
        {
            "title": "ChatGPT 블로그 글쓰기 도우미",
            "content": "당신은 전문 블로거입니다. 주제를 받으면 SEO에 최적화된 블로그 글을 작성해주세요. 다음 구조를 따라주세요:\n\n1. 흥미로운 제목\n2. 서론 (문제 제기)\n3. 본론 (3-4개 소제목)\n4. 결론 및 행동 유도\n\n주제: [여기에 주제 입력]",
            "description": "SEO 최적화된 블로그 글을 작성해주는 프롬프트입니다. 구조화된 글쓰기로 높은 품질의 콘텐츠를 만들 수 있습니다.",
            "category_id": 1,
            "ai_model_key": "gpt4",
            "tags": ["블로그", "SEO", "글쓰기", "콘텐츠"],
            "tier": "basic",
            "difficulty_level": 1
        },
        {
            "title": "코딩 문제 해결 전문가",
            "content": "당신은 시니어 개발자입니다. 사용자가 코딩 문제나 에러를 제시하면:\n\n1. 문제 분석\n2. 원인 파악\n3. 해결 방법 제시 (여러 옵션)\n4. 코드 예시\n5. 추가 개선 사항\n\n코드는 주석과 함께 설명해주세요.\n\n문제: [여기에 문제 설명]",
            "description": "프로그래밍 문제를 체계적으로 해결해주는 프롬프트입니다. 초보자도 이해하기 쉽게 설명합니다.",
            "category_id": 8,
            "ai_model_key": "gpt4",
            "tags": ["코딩", "프로그래밍", "디버깅", "개발"],
            "tier": "premium",
            "difficulty_level": 2
        },
        {
            "title": "창작 스토리 아이디어 생성기",
            "content": "당신은 창의적인 작가입니다. 다음 요소들을 조합해서 흥미진진한 스토리 아이디어를 만들어주세요:\n\n- 장르: [판타지/SF/로맨스/스릴러 등]\n- 주인공: [나이, 직업, 특징]\n- 배경: [시대, 장소]\n- 갈등: [주요 문제상황]\n\n3개의 서로 다른 스토리 아이디어를 제시하고, 각각의 매력 포인트를 설명해주세요.",
            "description": "소설, 웹툰, 영화 등의 창작 아이디어를 생성해주는 프롬프트입니다. 다양한 장르에 활용 가능합니다.",
            "category_id": 4,
            "ai_model_key": "claude",
            "tags": ["창작", "스토리", "아이디어", "소설"],
            "tier": "basic",
            "difficulty_level": 1
        },
        {
            "title": "Midjourney 이미지 생성 프롬프트",
            "content": "다음 스타일로 이미지를 생성해주세요:\n\n/imagine prompt: [주제] in [스타일], [분위기], [색상 톤], [구도], [조명], ultra detailed, 8k resolution, photorealistic, cinematic lighting, --ar 16:9 --v 5.2\n\n예시:\n/imagine prompt: mystical forest in anime style, ethereal atmosphere, emerald and gold tones, wide angle shot, soft moonlight filtering through trees, ultra detailed, 8k resolution, photorealistic, cinematic lighting, --ar 16:9 --v 5.2",
            "description": "Midjourney에서 고품질 이미지를 생성하기 위한 상세한 프롬프트 템플릿입니다.",
            "category_id": 2,
            "ai_model_key": "midjourney",
            "tags": ["Midjourney", "이미지생성", "AI아트", "프롬프트"],
            "tier": "featured",
            "difficulty_level": 2
        },
        {
            "title": "업무 이메일 작성 도우미",
            "content": "당신은 비즈니스 커뮤니케이션 전문가입니다. 다음 정보를 바탕으로 전문적인 업무 이메일을 작성해주세요:\n\n- 받는 사람: [이름/직책]\n- 목적: [이메일 목적]\n- 주요 내용: [전달할 내용]\n- 톤: [공식적/친근함/긴급함]\n\n이메일 구조:\n1. 적절한 인사말\n2. 목적 명시\n3. 주요 내용 (명확하고 간결하게)\n4. 다음 단계 또는 요청사항\n5. 정중한 마무리",
            "description": "비즈니스 상황에 맞는 전문적인 이메일을 작성해주는 프롬프트입니다. 다양한 업무 상황에 활용 가능합니다.",
            "category_id": 3,
            "ai_model_key": "gpt35",
            "tags": ["이메일", "업무", "비즈니스", "커뮤니케이션"],
            "tier": "basic",
            "difficulty_level": 1
        }
    ]
    
    prompts = []
    for i, prompt_data in enumerate(sample_prompts):
        # 랜덤하게 사용자 할당
        user = random.choice(users)
        
        prompt = PromptCard(
            prompt_id=f"prompt_{str(uuid.uuid4())[:8]}",
            user_id=user.user_id,
            title=prompt_data["title"],
            content=prompt_data["content"],
            description=prompt_data["description"],
            category_id=prompt_data["category_id"],
            ai_model_key=prompt_data["ai_model_key"],
            tags=prompt_data["tags"],
            tier=prompt_data["tier"],
            difficulty_level=prompt_data["difficulty_level"],
            views=random.randint(50, 1000),
            likes=random.randint(5, 100),
            bookmarks=random.randint(2, 50),
            shares=random.randint(1, 20),
            comments_count=random.randint(0, 15),
            created_at=datetime.now() - timedelta(days=random.randint(1, 30)),
            updated_at=datetime.now(),
            status="published"
        )
        prompts.append(prompt)
    
    return prompts

def initialize_sample_data():
    """샘플 데이터 초기화"""
    print("📊 샘플 데이터 생성 중...")
    
    # 사용자 데이터 생성
    users = generate_sample_users()
    user_manager = UserManager()
    user_manager.save_all(users)
    print(f"✅ {len(users)}명의 사용자 데이터 생성 완료")
    
    # 프롬프트 데이터 생성
    prompts = generate_sample_prompts(users)
    prompt_manager = PromptManager()
    prompt_manager.save_all(prompts)
    print(f"✅ {len(prompts)}개의 프롬프트 데이터 생성 완료")
    
    print("🎉 모든 샘플 데이터 생성이 완료되었습니다!")

if __name__ == "__main__":
    initialize_sample_data()