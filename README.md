# 🏫 학교 급식 메뉴 자동 전송 봇

Slack에 매일 자동으로 학교 급식 메뉴를 전송하는 봇입니다.

## 기능

- 학교 홈페이지에서 메뉴 크롤링
- 매일 자동으로 Slack에 메뉴 전송
- GitHub Actions를 통한 무료 자동 실행

## 설치 방법

### 1. 저장소 클론 및 의존성 설치

```bash
cd today-menu-bot
pip install -r requirements.txt
```

### 2. Slack Webhook URL 생성

1. [Slack API 웹사이트](https://api.slack.com/apps)에 접속
2. 앱 선택 (또는 새로 생성)
3. 좌측 메뉴에서 "Incoming Webhooks" 선택
4. "Activate Incoming Webhooks" 토글 활성화
5. "Add New Webhook to Workspace" 클릭
6. 메시지를 받을 채널 선택
7. 생성된 Webhook URL 복사 (예: `https://hooks.slack.com/services/XXXX/YYYY/ZZZZ`)

### 3. 환경 변수 설정

프로젝트 루트에 `.env` 파일을 생성하고 다음 내용을 입력:

```env
# Webhook 모드용 (자동 알림)
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXXX/YYYY/ZZZZ

# 학교 메뉴 설정
SCHOOL_MENU_WEBSITE_URL=https://mportal2.cau.ac.kr/main.do
```

- `SLACK_WEBHOOK_URL`: 위에서 복사한 Webhook URL
- `SCHOOL_MENU_WEBSITE_URL`: 학교 홈페이지 급식 메뉴 페이지 URL

## 실행 방법

### 로컬에서 테스트

```bash
python main.py
```

이 스크립트는 학교 홈페이지에서 메뉴를 크롤링하여 Slack Webhook으로 전송합니다.

## 학교 홈페이지 크롤링 설정

이 봇은 AngularJS로 동적 생성되는 페이지를 크롤링하기 위해 **Selenium**을 사용합니다.

### 자동 크롤링

현재 구현된 코드는 다음을 자동으로 수행합니다:
- 조식/중식/석식 탭을 각각 클릭하여 메뉴 추출
- `.nb-p-04-03` 클래스의 메뉴 항목 파싱
- 중복 제거 및 정리

### 커스터마이징

학교 홈페이지 구조가 다른 경우 `menu_fetcher.py`의 `_fetch_from_website` 메서드를 수정해야 합니다.

1. 크롬 브라우저에서 학교 식단표 페이지에 접속
2. `F12`를 눌러 개발자 도구 열기
3. 메뉴 부분에 마우스 우클릭 → "검사(Inspect)" 클릭
4. 해당 HTML 태그의 Class나 ID 확인
5. `_fetch_from_website` 메서드에서 선택자 수정

### 로컬 테스트

로컬에서 테스트할 때는 Chrome 브라우저가 설치되어 있어야 합니다:
- Windows/Mac: Chrome 브라우저 설치
- Linux: `sudo apt-get install google-chrome-stable` (또는 해당 배포판의 패키지 매니저 사용)

ChromeDriver는 `webdriver-manager`가 자동으로 다운로드합니다.

## GitHub Actions로 자동 실행 설정

매일 자동으로 메뉴를 전송하려면 GitHub Actions를 사용할 수 있습니다.

### 1. GitHub 리포지토리 생성 및 코드 업로드

1. GitHub에 새 리포지토리 생성
2. 코드 업로드

### 2. GitHub Secrets 설정

리포지토리 Settings → Secrets and variables → Actions에서 다음 Secrets 추가:

- `SLACK_WEBHOOK_URL`: Slack Webhook URL (필수)
- `SCHOOL_MENU_WEBSITE_URL`: 학교 홈페이지 급식 메뉴 URL (필수)
- `SCHOOL_CODE`: 학교 코드 (선택사항)
- `SCHOOL_MENU_API_URL`: 학교 API URL (선택사항)

### 3. 실행 시간 조정

`.github/workflows/run_bot.yml` 파일에서 실행 시간을 조정할 수 있습니다:

```yaml
- cron: '0 22 * * *' # 매일 오전 7시(KST) 실행 → 9시(KST) 알람 도착 예상
```

UTC 기준 시간이므로 한국 시간(KST)에서 9시간을 빼야 합니다.
- 한국 시간 오전 7시 → UTC 22:00 (전날)

### 4. 수동 실행

GitHub Actions 탭에서 "학식 알림 봇" 워크플로우를 선택하고 "Run workflow" 버튼을 클릭하여 수동으로 실행할 수 있습니다.

## 학교 급식 API 연동

실제 학교 급식 데이터를 사용하려면 `menu_fetcher.py`의 `_fetch_from_api` 메서드를 수정하거나, 학교 급식 API를 제공하는 서비스를 사용하세요.

한국의 경우 다음 API를 사용할 수 있습니다:
- [나이스 교육정보 개방 포털](https://open.neis.go.kr/) - NEIS 급식 API
- 기타 학교별 급식 API

## 커스터마이징

### 메뉴 포맷 변경

`menu_fetcher.py`의 `format_menu_message` 메서드를 수정하여 메시지 형식을 변경할 수 있습니다.

## 문제 해결

### 메뉴가 전송되지 않는 경우

1. `.env` 파일의 `SLACK_WEBHOOK_URL`이 올바른지 확인
2. GitHub Secrets에 `SLACK_WEBHOOK_URL`이 설정되어 있는지 확인
3. Slack Webhook이 활성화되어 있는지 확인

### 크롤링 오류가 발생하는 경우

1. Chrome 브라우저가 설치되어 있는지 확인
2. `SCHOOL_MENU_WEBSITE_URL`이 올바른지 확인
3. 학교 홈페이지 구조가 변경되었는지 확인

## 라이선스

MIT
