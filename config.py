import os
from dotenv import load_dotenv

load_dotenv()

# Slack Configuration (봇 모드 제거됨 - 자동 전송만 사용)
# SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
# SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

# School Menu Configuration
SCHOOL_MENU_API_URL = os.getenv("SCHOOL_MENU_API_URL", "")
SCHOOL_CODE = os.getenv("SCHOOL_CODE", "")
SCHOOL_MENU_WEBSITE_URL = os.getenv("SCHOOL_MENU_WEBSITE_URL", "")

# Slack Webhook Configuration (for scheduled notifications)
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")

# Selenium Configuration
# 로컬 환경에서는 자동으로 false (브라우저 창 표시)
# 서버 환경(GitHub Actions)에서는 자동으로 true (헤드리스 모드)
import platform
if os.getenv("SELENIUM_HEADLESS"):
    # 환경 변수가 명시적으로 설정된 경우 그 값 사용
    SELENIUM_HEADLESS = os.getenv("SELENIUM_HEADLESS").lower() == "true"
else:
    # 환경 변수가 없으면 플랫폼에 따라 자동 설정
    # Linux = 서버 환경 (헤드리스), Windows/Mac = 로컬 환경 (브라우저 표시)
    SELENIUM_HEADLESS = platform.system() == "Linux"

# Validate required tokens
# 검증은 각 모듈에서 필요할 때 수행하도록 변경
# (app.py는 SLACK_BOT_TOKEN 필요, main.py는 SLACK_WEBHOOK_URL 필요)
# import 시점에는 검증하지 않음

