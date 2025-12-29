import os
from dotenv import load_dotenv

load_dotenv()

# Slack Configuration
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

# School Menu Configuration
SCHOOL_MENU_API_URL = os.getenv("SCHOOL_MENU_API_URL", "")
SCHOOL_CODE = os.getenv("SCHOOL_CODE", "")
SCHOOL_MENU_WEBSITE_URL = os.getenv("SCHOOL_MENU_WEBSITE_URL", "")

# Slack Webhook Configuration (for scheduled notifications)
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")

# Selenium Configuration
# 테스트할 때는 "false"로 설정하면 브라우저 창이 뜹니다
# 서버(GitHub Actions)에 올릴 때는 "true"로 설정하거나 비워두세요
SELENIUM_HEADLESS = os.getenv("SELENIUM_HEADLESS", "true").lower() == "true"

# Validate required tokens
# 검증은 각 모듈에서 필요할 때 수행하도록 변경
# (app.py는 SLACK_BOT_TOKEN 필요, main.py는 SLACK_WEBHOOK_URL 필요)
# import 시점에는 검증하지 않음

