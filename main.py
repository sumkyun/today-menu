"""
학교 홈페이지에서 메뉴를 크롤링하여 Slack Webhook으로 전송하는 스크립트
GitHub Actions에서 매일 자동 실행되도록 설계됨
"""
import sys
# Windows 인코딩 문제 해결
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from webhook_sender import WebhookSender
from config import SLACK_WEBHOOK_URL


def main():
    """메인 실행 함수"""
    if not SLACK_WEBHOOK_URL:
        print("❌ SLACK_WEBHOOK_URL이 설정되지 않았습니다.")
        print("   .env 파일에 SLACK_WEBHOOK_URL을 설정해주세요.")
        return
    
    try:
        sender = WebhookSender()
        success = sender.send_today_menu()
        
        if success:
            print("✅ 전송 완료")
        else:
            print("❌ 전송 실패")
            exit(1)
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        exit(1)


if __name__ == "__main__":
    main()

