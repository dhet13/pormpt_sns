## Promptub (PromShare)

🚀 **[Live Demo - pormptsns-production.up.railway.app](https://pormptsns-production.up.railway.app)**


## 🚀 프로젝트 실행 방법

### Flet 설치 및 실행
```bash
# Flet 설치
pip install flet

# 로컬 데스크톱 앱으로 실행
python app.py

# 웹 브라우저로 실행
flet run app.py --web
```

### Flet 사용 이유
- **Flutter 기반**: Google의 Flutter 프레임워크를 Python으로 사용할 수 있게 해주는 프레임워크
- **크로스 플랫폼**: 하나의 코드로 데스크톱(Windows, macOS, Linux), 웹, 모바일 앱 개발 가능
- **빠른 프로토타이핑**: Python의 간결함과 Flutter의 성능을 결합하여 신속한 개발 가능
- **네이티브 성능**: Flutter 엔진을 사용하여 네이티브 수준의 성능 제공

## 🤖 프로젝트 진행 내용

이 프로젝트는 **AI 어시스턴트와의 협업**을 통해 개발되고 있습니다:

- **AI 기반 개발**: Claude Sonnet을 활용한 페어 프로그래밍 방식으로 진행
- **TDD 방식**: 테스트 우선 개발(Test-Driven Development) 적용
- **점진적 개발**: MVP부터 시작하여 단계별 기능 확장
- **실시간 피드백**: AI와의 대화를 통한 즉각적인 코드 리뷰 및 개선
- **문서화**: 개발 과정과 의사결정 과정을 상세히 기록

### 현재 개발 완료 기능
- ✅ 기본 UI 프레임워크 구축 (Flet 0.28.3 호환)
- ✅ 프롬프트 카드 그리드 레이아웃 (3열)
- ✅ 카드 호버 효과 및 애니메이션
- ✅ 모달 팝업을 통한 상세보기
- ✅ CSV 기반 데이터 관리 시스템
- ✅ 사용자 인증 시스템 기초

### 진행 예정 기능
- 🔄 좋아요/북마크/공유/조회수 기능
- 🔄 AI/카테고리 뱃지 필터링
- 🔄 포인트 시스템 (라이트 버전)
- 🔄 썸네일 이미지 로딩
- 🔄 헤더 검색 기능

## 📋 프로젝트 개요

### 1) 서비스 컨셉
- **서비스명**: Promptub (PromShare)
- **컨셉**: 프롬프트 공유 중심 SNS → 인기 프롬프트 유료화 → 프롬프트 거래 마켓
- **목표**: 한국어 기반 + 글로벌 확장 가능한 AI 프롬프트 허브 구축

### 2) 차별화 포인트
- **한국어 최적화** 및 국내 모델(CLOVA X, KoGPT) 지원
- **산업·업무·취미별** 세분화 카테고리
- **포인트·레벨·뱃지** 기반 게임화
- 해외 인기 프롬프트 **번역·현지화** 기능

### 3) 추진 전략
- **SNS → 마켓플레이스 순서**
  - 초기: 무료 프롬프트 공유 중심 SNS
  - 이후: 인기 프롬프트 유료화 + 제작자 수익 구조
  - 최종: 완전한 프롬프트 거래 마켓

### 4) SNS 단계 핵심 기능
- 프롬프트 업로드(제목, 설명, 결과 예시, 태그, AI 모델)
- 좋아요, 댓글, 북마크, 공유
- 팔로우/팔로잉, 태그·카테고리 검색
- 인기/최신 피드

### 5) 확장 기능(이후 단계)
- 프롬프트 실행 테스트기(개인 API 키 연동)
- 프롬프트 번역(영↔한)
- 프롬프트 시리즈(묶음 공유)

### 6) 보상 & 게임화
- **가시적 보상**: 뱃지, 인증 마크, 프로필 꾸미기, 노출 우선권
- **실질적 보상**: 포인트 환전, AI 크레딧, 유료 프롬프트 무료 이용권, 굿즈/행사 초대
- **포인트 예시**
  - 프롬프트 작성: +50
  - 조회 100회 달성: +20
  - 좋아요 받음: +5
  - 댓글 작성: +3
  - 공유: +10
  - 출석: +5
  - 일일 최대 300점 한도
- **레벨 예시**
  - Lv.1 Rookie → Lv.5 Contributor → Lv.10 Influencer → Lv.20 Master → Lv.30 Legend
  - 레벨별 혜택: 꾸미기, 수익 배분율 증가, 상단 노출

### 7) 브랜드
- **서비스명**: Promptub (Prompt + Hub)
- **브랜드 방향**: 네트워크 허브 메타포, 글로벌 친화적 발음과 짧은 이름
- **슬로건 예시**
  - Promptub — Where Prompts Connect
  - Promptub — Your AI Creativity Hub

---

## 🔧 프로토타입(현재 레포) 운영 원칙
- **프레임워크**: Flet 기반 데스크톱/웹 앱 프로토타입
- **데이터 저장**: 초기엔 CSV(로컬) 사용 후 서버/DB로 마이그레이션
- **개발 방식**: TDD(테스트 우선) + 점진적 기능 확장
- **AI 모델 선택**: API 연동 없이 모델 선택 → 외부 AI 페이지 새창 링크
- **포인트 경제**: 조회 시 포인트 차감(남용 방지), 출석/작성/기여 보상(보수적 설정)
- **SEO 정책**: 최소한의 메타만 유지, 크롤러 접근 제한(운영 배포 시 robots 정책 적용)

### CSV 데이터 스키마(초기)
- users.csv, prompts.csv, categories.csv, interactions.csv, tags.csv, comments.csv, likes.csv,
  settings.csv, notifications.csv, messages.csv, user_actions.csv, abuse_reports.csv

### 현재 레포 구조(요약)
```
promshare/
  app.py
  components/
    __init__.py
    main_page.py
    prompt_card.py
    header.py
  managers/
    prompt_manager.py
    user_manager.py
  services/
    prompt_service.py
    user_service.py
  data/
    prompts.csv
    users.csv
  README.md
```
