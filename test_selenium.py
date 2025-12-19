"""
Selenium 크롤링 테스트 스크립트
버튼 클릭이 제대로 작동하는지 테스트할 수 있습니다.
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from config import SCHOOL_MENU_WEBSITE_URL, SELENIUM_HEADLESS


def test_menu_with_selenium():
    """
    Selenium을 사용하여 메뉴를 가져오는 테스트 함수
    이 함수는 버튼 클릭이 제대로 작동하는지 확인하는 데 사용됩니다.
    """
    # 1. 크롬 옵션 설정
    chrome_options = Options()
    
    # 테스트할 때는 headless를 False로 설정하면 브라우저 창이 뜹니다
    # 나중에 서버에 올릴 때는 True로 설정하세요
    if SELENIUM_HEADLESS:
        chrome_options.add_argument("--headless")
        print("🔧 Headless 모드 활성화 (브라우저 창이 뜨지 않습니다)")
    else:
        print("🔧 Headless 모드 비활성화 (브라우저 창이 뜹니다)")
    
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    # 2. 드라이버 자동 설치 및 실행
    # webdriver-manager가 Chrome 버전을 자동으로 감지하고 맞는 드라이버를 다운로드합니다
    # 이 부분이 'Chrome not installed' 오류를 해결합니다!
    print("🔍 ChromeDriver 자동 설치 중...")
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("✅ ChromeDriver 설정 완료")
    except Exception as e:
        print(f"❌ Chrome/ChromeDriver 설정 실패: {e}")
        print("\n💡 해결 방법:")
        print("   1. Chrome 브라우저가 설치되어 있는지 확인하세요")
        print("   2. Windows: Chrome이 기본 설치 경로에 있는지 확인")
        print("   3. Ubuntu/Debian: sudo apt-get install google-chrome-stable")
        print("   4. macOS: brew install --cask google-chrome")
        return

    try:
        # 3. 사이트 접속
        url = SCHOOL_MENU_WEBSITE_URL or "https://학교식단주소.ac.kr"  # config에서 가져오거나 직접 입력
        print(f"🌐 페이지 접속 중: {url}")
        driver.get(url)
        
        # 페이지 로딩 기다리기 (넉넉하게 3초)
        print("⏳ 페이지 로딩 대기 중...")
        time.sleep(3)

        # 4. 버튼 클릭하기 (여기가 중요!)
        # F12를 눌러서 개발자 도구에서 버튼의 selector를 찾아야 합니다
        # 예: id가 'today-btn'인 경우 -> By.ID, "today-btn"
        # 예: class가 'lunch'인 경우 -> By.CSS_SELECTOR, ".lunch"
        # 예: 텍스트가 '중식'인 경우 -> By.XPATH, "//em[contains(text(), '중식')]"
        
        wait = WebDriverWait(driver, 10)
        
        # [예시] "중식" 버튼을 클릭한다고 가정
        # 아래 selector는 실제 학교 홈페이지에 맞게 수정해야 합니다
        try:
            print("🔘 중식 탭 클릭 시도 중...")
            # XPath 예시: 텍스트가 '중식'인 em 태그 찾기
            lunch_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//em[contains(text(), '중식')]")))
            lunch_tab.click()
            print("✅ 중식 탭 클릭 성공!")
            
            # 클릭 후 데이터 로딩 기다리기
            time.sleep(2)
        except Exception as e:
            print(f"⚠️  중식 탭을 찾을 수 없습니다: {e}")
            print("\n💡 Selector 찾는 방법:")
            print("   1. 크롬에서 학교 식단 페이지 접속 후 F12를 누릅니다")
            print("   2. 왼쪽 위 화살표 아이콘(Elements 선택 도구)을 클릭합니다")
            print("   3. 클릭해야 하는 '버튼'이나 '탭'을 클릭합니다")
            print("   4. 오른쪽 코드 창에서 파랗게 표시된 부분에 우클릭 -> Copy -> Copy selector")
            print("   5. 복사한 내용을 위 코드의 selector 부분에 붙여넣습니다")

        # 5. 메뉴 텍스트 가져오기
        # 아래 selector도 실제 페이지 구조에 맞게 수정해야 합니다
        try:
            # 예시: 메뉴가 적힌 태그의 selector
            # menu_element = driver.find_element(By.CSS_SELECTOR, "메뉴가_적힌_태그_선택자")
            # menu_text = menu_element.text
            
            # 테스트용: 페이지 제목 가져오기
            page_title = driver.title
            print(f"📄 페이지 제목: {page_title}")
            
            # 페이지 소스 일부 확인
            page_source = driver.page_source[:500]  # 처음 500자만
            print(f"📝 페이지 소스 일부:\n{page_source}...")
            
        except Exception as e:
            print(f"⚠️  메뉴를 가져오는 중 오류: {e}")

        print("\n✅ 테스트 완료!")
        print("💡 브라우저가 자동으로 닫히기 전에 잠시 대기합니다...")
        if not SELENIUM_HEADLESS:
            print("   (브라우저 창을 확인하세요)")
            time.sleep(5)  # headless가 아닐 때는 5초 대기

    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        driver.quit()  # 크롬 끄기
        print("🔒 브라우저 종료")


if __name__ == "__main__":
    print("=" * 60)
    print("🧪 Selenium 크롤링 테스트 시작")
    print("=" * 60)
    print("\n💡 팁:")
    print("   - .env 파일에서 SELENIUM_HEADLESS=false로 설정하면")
    print("     브라우저 창이 뜨면서 동작을 확인할 수 있습니다")
    print("   - 버튼 selector를 찾으려면 F12를 눌러 개발자 도구를 사용하세요")
    print("=" * 60)
    print()
    
    test_menu_with_selenium()

