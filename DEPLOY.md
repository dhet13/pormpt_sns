# Netlify 배포 가이드

## 🚀 Netlify에 Flet 앱 배포하기

### 1. 준비 사항
- GitHub 계정 및 리포지토리
- Netlify 계정

### 2. 배포 단계

#### Step 1: GitHub에 코드 푸시
```bash
git add .
git commit -m "Add Netlify deployment configuration"
git push origin main
```

#### Step 2: Netlify에서 사이트 생성
1. [Netlify](https://netlify.com)에 로그인
2. "New site from Git" 클릭
3. GitHub 리포지토리 선택
4. 빌드 설정은 자동으로 `netlify.toml`에서 읽어옴

#### Step 3: 자동 배포 확인
- Netlify가 자동으로 빌드 및 배포 진행
- 빌드 로그에서 진행 상황 확인 가능

### 3. 빌드 설정 (netlify.toml)
```toml
[build]
  publish = "dist"
  command = "pip install -r requirements.txt && flet build web"

[build.environment]
  PYTHON_VERSION = "3.11"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### 4. 로컬에서 웹 빌드 테스트
```bash
# 의존성 설치
pip install -r requirements.txt

# 웹용 빌드
flet build web

# 빌드된 파일 확인
ls -la dist/
```

### 5. 주의사항

#### 파일 경로 문제
- CSV 파일 등 데이터 파일이 제대로 포함되는지 확인
- 상대 경로 사용 권장

#### 환경 변수 (필요한 경우)
- Netlify 대시보드에서 환경 변수 설정 가능
- Site settings > Environment variables

#### 도메인 설정
- 기본: `https://your-app-name.netlify.app`
- 커스텀 도메인 연결 가능

### 6. 문제 해결

#### 빌드 실패 시
1. Netlify 빌드 로그 확인
2. 로컬에서 `flet build web` 테스트
3. Python 버전 확인 (3.11 권장)

#### 라우팅 문제 시
- `netlify.toml`의 redirects 설정 확인
- SPA(Single Page Application) 설정 필요

### 7. 배포 후 확인사항
- [ ] 메인 페이지 로딩
- [ ] 카드 그리드 표시
- [ ] 모달 팝업 동작
- [ ] 반응형 레이아웃
- [ ] 라우팅 기능

### 8. 업데이트 배포
```bash
# 코드 수정 후
git add .
git commit -m "Update features"
git push origin main
# Netlify가 자동으로 재배포
```

---

## 💡 추가 팁

### 성능 최적화
- 이미지 최적화
- CSS/JS 압축 (Flet이 자동 처리)
- CDN 활용 (Netlify 기본 제공)

### 모니터링
- Netlify Analytics 활용
- 에러 로그 모니터링
- 성능 지표 확인

### 보안
- HTTPS 자동 적용 (Netlify 기본)
- 환경 변수로 민감 정보 관리
- CORS 설정 (필요시)
