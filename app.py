"""
Slack 학교 급식 메뉴 봇
"""
from datetime import datetime, timedelta
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from menu_fetcher import MenuFetcher
from config import SLACK_BOT_TOKEN, SLACK_APP_TOKEN

# 필수 토큰 검증
if not SLACK_BOT_TOKEN:
    raise ValueError("SLACK_BOT_TOKEN environment variable is required for bot mode")
if not SLACK_APP_TOKEN:
    raise ValueError("SLACK_APP_TOKEN environment variable is required for bot mode")

# Slack 앱 초기화
app = App(token=SLACK_BOT_TOKEN)

# 메뉴 페처 초기화
menu_fetcher = MenuFetcher()


@app.message("오늘 메뉴")
@app.message("오늘 급식")
@app.message("today menu")
@app.message("menu")
def handle_today_menu(message, say):
    """오늘의 급식 메뉴를 반환합니다."""
    try:
        menu_data = menu_fetcher.get_today_menu()
        formatted_message = menu_fetcher.format_menu_message(menu_data)
        say(formatted_message)
    except Exception as e:
        say(f"메뉴를 가져오는 중 오류가 발생했습니다: {str(e)}")


@app.action("menu_today")
def handle_menu_today(ack, body, respond):
    """오늘 메뉴 버튼 클릭 처리"""
    ack()
    try:
        menu_data = menu_fetcher.get_today_menu()
        formatted_message = menu_fetcher.format_menu_message(menu_data)
        respond(formatted_message)
    except Exception as e:
        respond(f"메뉴를 가져오는 중 오류가 발생했습니다: {str(e)}")


@app.action("menu_tomorrow")
def handle_menu_tomorrow(ack, body, respond):
    """내일 메뉴 버튼 클릭 처리"""
    ack()
    try:
        tomorrow = datetime.now() + timedelta(days=1)
        menu_data = menu_fetcher.get_menu_by_date(tomorrow)
        formatted_message = menu_fetcher.format_menu_message(menu_data)
        respond(formatted_message)
    except Exception as e:
        respond(f"메뉴를 가져오는 중 오류가 발생했습니다: {str(e)}")


@app.action("menu_day_after")
def handle_menu_day_after(ack, body, respond):
    """모레 메뉴 버튼 클릭 처리"""
    ack()
    try:
        day_after = datetime.now() + timedelta(days=2)
        menu_data = menu_fetcher.get_menu_by_date(day_after)
        formatted_message = menu_fetcher.format_menu_message(menu_data)
        respond(formatted_message)
    except Exception as e:
        respond(f"메뉴를 가져오는 중 오류가 발생했습니다: {str(e)}")


@app.command("/메뉴")
@app.command("/menu")
def handle_menu_command(ack, respond, command):
    """슬래시 커맨드로 메뉴를 조회합니다."""
    ack()
    
    try:
        # 날짜 파라미터가 있으면 해당 날짜, 없으면 버튼 제공
        date_param = command.get('text', '').strip()
        
        if date_param:
            # 날짜 파싱 (예: "2024-01-15" 또는 "내일", "모레" 등)
            if date_param == "내일":
                target_date = datetime.now() + timedelta(days=1)
            elif date_param == "모레":
                target_date = datetime.now() + timedelta(days=2)
            else:
                try:
                    target_date = datetime.strptime(date_param, "%Y-%m-%d")
                except ValueError:
                    respond("날짜 형식이 올바르지 않습니다. YYYY-MM-DD 형식으로 입력해주세요.")
                    return
            
            menu_data = menu_fetcher.get_menu_by_date(target_date)
            formatted_message = menu_fetcher.format_menu_message(menu_data)
            respond(formatted_message)
        else:
            # 파라미터가 없으면 버튼 제공
            respond(
                blocks=[
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "🍽️ *어떤 메뉴를 확인하시겠어요?*"
                        }
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "🌅 오늘 메뉴"
                                },
                                "value": "today",
                                "action_id": "menu_today"
                            },
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "📅 내일 메뉴"
                                },
                                "value": "tomorrow",
                                "action_id": "menu_tomorrow"
                            },
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "📆 모레 메뉴"
                                },
                                "value": "day_after",
                                "action_id": "menu_day_after"
                            }
                        ]
                    }
                ]
            )
    except Exception as e:
        respond(f"메뉴를 가져오는 중 오류가 발생했습니다: {str(e)}")


@app.event("app_mention")
def handle_mention(event, say):
    """봇이 멘션되었을 때 처리합니다."""
    text = event.get('text', '').lower()
    
    if any(keyword in text for keyword in ['메뉴', '급식', 'menu']):
        # 버튼이 포함된 메시지 전송
        say(
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "🍽️ *어떤 메뉴를 확인하시겠어요?*"
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "🌅 오늘 메뉴"
                            },
                            "value": "today",
                            "action_id": "menu_today"
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "📅 내일 메뉴"
                            },
                            "value": "tomorrow",
                            "action_id": "menu_tomorrow"
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "📆 모레 메뉴"
                            },
                            "value": "day_after",
                            "action_id": "menu_day_after"
                        }
                    ]
                }
            ]
        )
    else:
        # 일반 메시지에도 버튼 제공
        say(
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "안녕하세요! 🏫 *학교 급식 메뉴 봇*입니다.\n\n어떤 메뉴를 확인하시겠어요?"
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "🌅 오늘 메뉴"
                            },
                            "value": "today",
                            "action_id": "menu_today"
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "📅 내일 메뉴"
                            },
                            "value": "tomorrow",
                            "action_id": "menu_tomorrow"
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "📆 모레 메뉴"
                            },
                            "value": "day_after",
                            "action_id": "menu_day_after"
                        }
                    ]
                }
            ]
        )


@app.event("app_home_opened")
def handle_app_home_opened(client, event):
    """앱 홈이 열렸을 때 홈 탭을 업데이트합니다."""
    try:
        menu_data = menu_fetcher.get_today_menu()
        formatted_message = menu_fetcher.format_menu_message(menu_data)
        
        client.views_publish(
            user_id=event["user"],
            view={
                "type": "home",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*🏫 학교 급식 메뉴 봇*\n\n급식 메뉴를 확인할 수 있는 봇입니다."
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": formatted_message
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*사용 방법:*\n• `오늘 메뉴` 또는 `오늘 급식` 메시지 보내기\n• `/menu` 또는 `/메뉴` 슬래시 커맨드 사용\n• 봇을 멘션하고 '메뉴'라고 입력"
                        }
                    }
                ]
            }
        )
    except Exception as e:
        print(f"홈 탭 업데이트 중 오류: {e}")


if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    print("🚀 Slack 학교 급식 메뉴 봇이 시작되었습니다!")
    handler.start()

