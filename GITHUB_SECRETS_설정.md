# 🔐 GitHub Secrets 설정 가이드

GitHub Actions에서 자동으로 메뉴를 전송하려면 다음 Secrets를 설정해야 합니다.

## 📋 추가해야 할 Secrets 목록

### ✅ 필수 (Required)

#### 1. `SLACK_WEBHOOK_URL`
- **설명**: Slack Webhook URL (메뉴를 전송할 주소)
- **형식**: `https://hooks.slack.com/services/XXXX/YYYY/ZZZZ`
- **어디서 가져오나**: 
  - Slack API 웹사이트 → 앱 선택 → Incoming Webhooks → Webhook URL 복사
- **예시 값**: `https://hooks.slack.com/services/T08M32KTRUH/B0A4HXXXXX/YYYYYYYYYYYY`

#### 2. `SCHOOL_MENU_WEBSITE_URL`
- **설명**: 학교 홈페이지 급식 메뉴 페이지 URL
- **형식**: `https://학교도메인.ac.kr/급식메뉴경로`
- **예시 값**: `https://mportal2.cau.ac.kr/main.do`

### ⚠️ 선택사항 (Optional)

#### 3. `SCHOOL_CODE`
- **설명**: 학교 코드 (API를 사용하는 경우)
- **형식**: 문자열
- **기본값**: 비워두면 됨 (크롤링 모드 사용)

#### 4. `SCHOOL_MENU_API_URL`
- **설명**: 학교 급식 API URL (API를 사용하는 경우)
- **형식**: `https://api.example.com/menu`
- **기본값**: 비워두면 됨 (크롤링 모드 사용)

---

## 🚀 설정 방법

1. GitHub 리포지토리 페이지 접속
2. **Settings** 탭 클릭
3. 왼쪽 메뉴에서 **Secrets and variables** → **Actions** 클릭
4. **New repository secret** 버튼 클릭
5. 각 Secret을 하나씩 추가:

### Secret 1: SLACK_WEBHOOK_URL
```
Name: SLACK_WEBHOOK_URL
Secret: https://hooks.slack.com/services/XXXX/YYYY/ZZZZ
```

### Secret 2: SCHOOL_MENU_WEBSITE_URL
```
Name: SCHOOL_MENU_WEBSITE_URL
Secret: https://mportal2.cau.ac.kr/main.do
```

### Secret 3: SCHOOL_CODE (선택사항)
```
Name: SCHOOL_CODE
Secret: (학교 코드가 있다면 입력)
```

### Secret 4: SCHOOL_MENU_API_URL (선택사항)
```
Name: SCHOOL_MENU_API_URL
Secret: (API URL이 있다면 입력)
```

---

## ✅ 확인 방법

설정이 완료되면:
1. GitHub Actions 탭으로 이동
2. "학식 알림 봇" 워크플로우 선택
3. "Run workflow" 버튼 클릭하여 수동 실행
4. 성공하면 Slack에 메뉴가 전송됩니다!

---

## 📝 참고사항

- **SELENIUM_HEADLESS**는 코드에서 자동으로 설정되어 있어서 별도로 추가할 필요 없습니다.
- Webhook 모드(`main.py`)에서는 **SLACK_WEBHOOK_URL**만 있으면 됩니다.

---

## 🔒 보안 주의사항

⚠️ **절대 코드에 직접 URL이나 토큰을 적지 마세요!**
- `.env` 파일은 `.gitignore`에 포함되어 있어 Git에 올라가지 않습니다.
- 모든 민감한 정보는 GitHub Secrets에 저장하세요.
- Secrets는 암호화되어 저장되며, 워크플로우 실행 시에만 사용됩니다.
