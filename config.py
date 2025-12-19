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

# Validate required tokens (only for bot mode, not for webhook mode)
# These are optional if only using webhook mode
if not SLACK_BOT_TOKEN and not SLACK_WEBHOOK_URL:
    raise ValueError("Either SLACK_BOT_TOKEN or SLACK_WEBHOOK_URL environment variable is required")
if not SLACK_APP_TOKEN and not SLACK_WEBHOOK_URL:
    # APP_TOKEN is only needed for Socket Mode (bot mode)
    pass

