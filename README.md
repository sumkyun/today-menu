# 🏫 학교 급식 메뉴 Slack 봇

Slack에서 학교 급식 메뉴를 확인할 수 있는 봇입니다.

## 기능

### 봇 모드 (Socket Mode)
- 오늘의 급식 메뉴 조회
- 특정 날짜의 급식 메뉴 조회
- 슬래시 커맨드 지원 (`/menu`, `/메뉴`)
- 멘션을 통한 메뉴 조회
- 앱 홈 탭에서 메뉴 확인

### Webhook 모드 (자동 알림)
- 학교 홈페이지에서 메뉴 크롤링
- 매일 자동으로 Slack에 메뉴 전송
- GitHub Actions를 통한 무료 자동 실행

## 설치 방법

### 1. 저장소 클론 및 의존성 설치

```bash
cd today-menu-bot
pip install -r requirements.txt
```

### 2. Slack 앱 생성

1. [Slack API 웹사이트](https://api.slack.com/apps)에 접속
2. "Create New App" 클릭
3. "From scratch" 선택
4. 앱 이름과 워크스페이스 선택 후 생성

### 3. Bot Token 발급

1. 좌측 메뉴에서 "OAuth & Permissions" 선택
2. "Bot Token Scopes" 섹션에서 다음 권한 추가:
   - `app_mentions:read` - 멘션 이벤트 수신
   - `chat:write` - 메시지 전송
   - `commands` - 슬래시 커맨드 사용
   - `users:read` - 사용자 정보 읽기
   - `channels:history` - 채널 메시지 읽기 (선택사항)
   - `groups:history` - 그룹 메시지 읽기 (선택사항)
   - `im:history` - DM 메시지 읽기 (선택사항)
   - `mpim:history` - 멀티 DM 메시지 읽기 (선택사항)
3. "Install to Workspace" 클릭하여 워크스페이스에 설치
4. "Bot User OAuth Token" (xoxb-로 시작) 복사

### 4. App-Level Token 발급

1. 좌측 메뉴에서 "Basic Information" 선택
2. "App-Level Tokens" 섹션으로 스크롤
3. "Generate Token and Scopes" 클릭
4. Token 이름 입력 (예: "socket-mode")
5. `connections:write` 스코프 추가
6. 생성된 Token (xapp-로 시작) 복사

### 5. Socket Mode 활성화

1. 좌측 메뉴에서 "Socket Mode" 선택
2. "Enable Socket Mode" 토글 활성화
3. 위에서 생성한 App-Level Token 선택

### 6. 슬래시 커맨드 등록

1. 좌측 메뉴에서 "Slash Commands" 선택
2. "Create New Command" 클릭
3. 다음 커맨드 등록:
   - Command: `/menu`
   - Request URL: (비워둠 - Socket Mode 사용)
   - Short Description: "오늘의 급식 메뉴를 조회합니다"
   - Usage Hint: "[날짜] (예: 2024-01-15 또는 내일, 모레)"
4. "Save" 클릭

### 7. Slack Webhook URL 생성 (Webhook 모드용)

1. [Slack API 웹사이트](https://api.slack.com/apps)에서 앱 선택
2. 좌측 메뉴에서 "Incoming Webhooks" 선택
3. "Activate Incoming Webhooks" 토글 활성화
4. "Add New Webhook to Workspace" 클릭
5. 메시지를 받을 채널 선택
6. 생성된 Webhook URL 복사 (예: `https://hooks.slack.com/services/XXXX/YYYY/ZZZZ`)

### 8. 환경 변수 설정

프로젝트 루트에 `.env` 파일을 생성하고 다음 내용을 입력:

```env
# 봇 모드용 (Socket Mode)
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_APP_TOKEN=xapp-your-app-token-here

# Webhook 모드용 (자동 알림)
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXXX/YYYY/ZZZZ

# 학교 메뉴 설정
SCHOOL_MENU_WEBSITE_URL=https://www.학교도메인.ac.kr/food/menu
SCHOOL_MENU_API_URL=
SCHOOL_CODE=
```

- `SLACK_BOT_TOKEN`: 위에서 복사한 Bot User OAuth Token (봇 모드용)
- `SLACK_APP_TOKEN`: 위에서 복사한 App-Level Token (봇 모드용)
- `SLACK_WEBHOOK_URL`: 위에서 복사한 Webhook URL (Webhook 모드용)
- `SCHOOL_MENU_WEBSITE_URL`: 학교 홈페이지 급식 메뉴 페이지 URL
- `SCHOOL_MENU_API_URL`: 학교 급식 API URL (선택사항)
- `SCHOOL_CODE`: 학교 코드 (선택사항)

## 실행 방법

### 봇 모드 (Socket Mode)

```bash
python app.py
```

봇이 정상적으로 실행되면 "🚀 Slack 학교 급식 메뉴 봇이 시작되었습니다!" 메시지가 출력됩니다.

### Webhook 모드 (자동 알림)

```bash
python main.py
```

이 스크립트는 학교 홈페이지에서 메뉴를 크롤링하여 Slack Webhook으로 전송합니다.

## 사용 방법

### 1. 버튼으로 조회 (추천! 🎯)

봇을 멘션하거나 `/menu` 명령어를 입력하면 버튼이 나타납니다:
- 🌅 **오늘 메뉴** 버튼 - 오늘의 급식 메뉴 확인
- 📅 **내일 메뉴** 버튼 - 내일의 급식 메뉴 확인
- 📆 **모레 메뉴** 버튼 - 모레의 급식 메뉴 확인

원하는 버튼을 클릭하면 해당 날짜의 메뉴가 표시됩니다!

### 2. 메시지로 조회

봇이 있는 채널에서 다음 중 하나를 입력:
- `오늘 메뉴`
- `오늘 급식`
- `today menu`
- `menu`

### 3. 슬래시 커맨드로 조회

- `/menu` - 버튼 메뉴 표시 (또는 오늘의 메뉴 조회)
- `/menu 2024-01-15` - 특정 날짜의 메뉴 조회
- `/menu 내일` - 내일의 메뉴 조회
- `/menu 모레` - 모레의 메뉴 조회

### 4. 멘션으로 조회

봇을 멘션하고 "메뉴" 또는 "급식"이라고 입력하면 버튼이 나타납니다.

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

- `SLACK_WEBHOOK_URL`: Slack Webhook URL
- `SCHOOL_MENU_WEBSITE_URL`: 학교 홈페이지 급식 메뉴 URL (선택사항)
- `SCHOOL_CODE`: 학교 코드 (선택사항)

### 3. 실행 시간 조정

`.github/workflows/run_bot.yml` 파일에서 실행 시간을 조정할 수 있습니다:

```yaml
- cron: '0 2 * * 1-5' # 월~금(1-5) 오전 11시(KST) 실행
```

UTC 기준 시간이므로 한국 시간(KST)에서 9시간을 빼야 합니다.
- 한국 시간 오전 11시 → UTC 02:00
- 한국 시간 오전 9시 → UTC 00:00

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

### 추가 명령어 추가

`app.py`에 새로운 메시지 핸들러나 커맨드를 추가할 수 있습니다.

## 문제 해결

### 봇이 응답하지 않는 경우

1. `.env` 파일의 토큰이 올바른지 확인
2. Socket Mode가 활성화되어 있는지 확인
3. 봇이 워크스페이스에 설치되어 있는지 확인
4. 봇이 채널에 초대되어 있는지 확인

### 권한 오류가 발생하는 경우

Slack 앱 설정에서 필요한 스코프가 모두 추가되어 있는지 확인하세요.

## 라이선스

MIT

