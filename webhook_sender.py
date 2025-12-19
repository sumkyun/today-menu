"""
Slack Webhook을 통해 메시지를 전송하는 모듈
"""
import json
import requests
from datetime import datetime
from typing import Dict, Optional
from config import SLACK_WEBHOOK_URL
from menu_fetcher import MenuFetcher


class WebhookSender:
    """Slack Webhook 메시지 전송 클래스"""
    
    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url or SLACK_WEBHOOK_URL
        if not self.webhook_url:
            raise ValueError("SLACK_WEBHOOK_URL이 설정되지 않았습니다.")
        self.menu_fetcher = MenuFetcher()
    
    def send_today_menu(self) -> bool:
        """
        오늘의 급식 메뉴를 Slack으로 전송합니다.
        
        Returns:
            bool: 전송 성공 여부
        """
        try:
            menu_data = self.menu_fetcher.get_today_menu()
            message = self._format_webhook_message(menu_data)
            return self._send_message(message)
        except Exception as e:
            print(f"메뉴 전송 중 오류 발생: {e}")
            return False
    
    def _format_webhook_message(self, menu_data: Dict[str, any]) -> str:
        """
        Webhook용 메시지를 포맷팅합니다.
        menu_fetcher의 format_menu_message를 사용하여 일관된 포맷 유지.
        
        Args:
            menu_data: 메뉴 정보 딕셔너리
            
        Returns:
            str: 포맷팅된 메시지
        """
        # menu_fetcher의 포맷팅 메서드 재사용
        return self.menu_fetcher.format_menu_message(menu_data)
    
    def _send_message(self, text: str) -> bool:
        """
        Slack Webhook으로 메시지를 전송합니다.
        
        Args:
            text: 전송할 메시지 텍스트
            
        Returns:
            bool: 전송 성공 여부
        """
        try:
            payload = {
                "text": text
            }
            
            response = requests.post(
                self.webhook_url,
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            response.raise_for_status()
            print("✅ Slack으로 메뉴 전송 완료!")
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Slack 메시지 전송 실패: {e}")
            return False

