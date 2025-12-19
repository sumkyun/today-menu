"""
Slack으로 메뉴 전송 테스트
"""
import sys
# Windows 인코딩 문제 해결
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from webhook_sender import WebhookSender
from config import SLACK_WEBHOOK_URL

def test_send():
    print("=" * 60)
    print("Slack 메뉴 전송 테스트")
    print("=" * 60)
    
    if not SLACK_WEBHOOK_URL:
        print("\nSLACK_WEBHOOK_URL이 설정되지 않았습니다.")
        print(".env 파일에 SLACK_WEBHOOK_URL을 설정해주세요.")
        return
    
    print(f"\nWebhook URL: {SLACK_WEBHOOK_URL[:50]}...")
    print("\n메뉴를 가져와서 전송 중...")
    
    try:
        sender = WebhookSender()
        success = sender.send_today_menu()
        
        if success:
            print("\n전송 완료!")
        else:
            print("\n전송 실패")
    except Exception as e:
        print(f"\n오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_send()

