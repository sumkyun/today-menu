"""
크롤링이 잘 작동하는지 테스트하는 스크립트
"""
import os
import sys
# Windows 인코딩 문제 해결
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from menu_fetcher import MenuFetcher
from config import SCHOOL_MENU_WEBSITE_URL

def test_crawling():
    """크롤링 테스트"""
    print("=" * 60)
    print("🧪 크롤링 테스트 시작")
    print("=" * 60)
    
    # 설정 확인
    print("\n📋 현재 설정:")
    print(f"   SCHOOL_MENU_WEBSITE_URL: {SCHOOL_MENU_WEBSITE_URL or '(설정되지 않음)'}")
    
    if not SCHOOL_MENU_WEBSITE_URL:
        print("\n⚠️  SCHOOL_MENU_WEBSITE_URL이 설정되지 않았습니다.")
        print("   .env 파일에 SCHOOL_MENU_WEBSITE_URL을 설정해주세요.")
        print("   예: SCHOOL_MENU_WEBSITE_URL=https://www.학교도메인.ac.kr/food/menu")
        return
    
    # MenuFetcher 초기화
    print("\n🔧 MenuFetcher 초기화 중...")
    fetcher = MenuFetcher()
    
    # 오늘 메뉴 가져오기 시도
    print("\n📥 오늘의 메뉴 가져오기 시도 중...")
    try:
        menu_data = fetcher.get_today_menu()
        
        print("\n✅ 크롤링 성공!")
        print("=" * 60)
        print("\n📊 가져온 메뉴 정보:")
        print(f"   날짜: {menu_data.get('date', 'N/A')}")
        
        # 조식
        breakfast = menu_data.get('breakfast', {})
        if isinstance(breakfast, dict):
            print(f"   조식: {len(breakfast)}개 식당")
            for restaurant, courses in breakfast.items():
                print(f"      - {restaurant}: {len(courses)}개 코스")
        elif isinstance(breakfast, list):
            print(f"   조식: {len(breakfast)}개 메뉴 항목")
        
        # 중식
        lunch = menu_data.get('lunch', {})
        if isinstance(lunch, dict):
            print(f"   중식: {len(lunch)}개 식당")
            for restaurant, courses in lunch.items():
                print(f"      - {restaurant}: {len(courses)}개 코스")
        elif isinstance(lunch, list):
            print(f"   중식: {len(lunch)}개 메뉴 항목")
        
        # 석식
        dinner = menu_data.get('dinner', {})
        if isinstance(dinner, dict):
            print(f"   석식: {len(dinner)}개 식당")
            for restaurant, courses in dinner.items():
                print(f"      - {restaurant}: {len(courses)}개 코스")
        elif isinstance(dinner, list):
            print(f"   석식: {len(dinner)}개 메뉴 항목")
        
        # 포맷팅된 메시지 확인
        print("\n" + "=" * 60)
        print("📝 포맷팅된 메시지 미리보기:")
        print("=" * 60)
        formatted = fetcher.format_menu_message(menu_data)
        print(formatted[:500] + "..." if len(formatted) > 500 else formatted)
        
        print("\n✅ 모든 테스트 통과!")
        
    except Exception as e:
        print(f"\n❌ 크롤링 실패: {e}")
        print("\n💡 문제 해결 방법:")
        print("   1. Chrome 브라우저가 설치되어 있는지 확인")
        print("   2. .env 파일에 SCHOOL_MENU_WEBSITE_URL이 올바르게 설정되었는지 확인")
        print("   3. 인터넷 연결 상태 확인")
        print("   4. 학교 홈페이지가 접속 가능한지 확인")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_crawling()

