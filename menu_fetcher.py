"""
학교 급식 메뉴를 가져오는 모듈
"""
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import time
import platform
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from config import SCHOOL_MENU_API_URL, SCHOOL_CODE, SCHOOL_MENU_WEBSITE_URL, SELENIUM_HEADLESS


class MenuFetcher:
    """학교 급식 메뉴를 가져오는 클래스"""
    
    def __init__(self):
        self.api_url = SCHOOL_MENU_API_URL
        self.school_code = SCHOOL_CODE
        self.website_url = SCHOOL_MENU_WEBSITE_URL
    
    def get_today_menu(self) -> Dict[str, any]:
        """
        오늘의 급식 메뉴를 가져옵니다.
        
        Returns:
            Dict: 메뉴 정보를 담은 딕셔너리
                {
                    'date': 'YYYY-MM-DD',
                    'breakfast': ['메뉴1', '메뉴2', ...],
                    'lunch': ['메뉴1', '메뉴2', ...],
                    'dinner': ['메뉴1', '메뉴2', ...]
                }
        """
        today = datetime.now()
        return self.get_menu_by_date(today)
    
    def get_menu_by_date(self, date: datetime) -> Dict[str, any]:
        """
        특정 날짜의 급식 메뉴를 가져옵니다.
        
        Args:
            date: 날짜 객체
            
        Returns:
            Dict: 메뉴 정보를 담은 딕셔너리
        """
        date_str = date.strftime("%Y-%m-%d")
        
        # API가 설정되어 있으면 API에서 가져오기
        if self.api_url:
            return self._fetch_from_api(date_str)
        
        # 웹사이트 URL이 설정되어 있으면 크롤링으로 가져오기
        if self.website_url:
            return self._fetch_from_website(date_str)
        
        # API가 없으면 샘플 데이터 반환 (실제 구현 시 학교 API로 교체)
        return self._get_sample_menu(date_str)
    
    def _fetch_from_api(self, date_str: str) -> Dict[str, any]:
        """API에서 메뉴를 가져옵니다."""
        try:
            params = {
                'date': date_str,
                'school_code': self.school_code
            }
            response = requests.get(self.api_url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            return {
                'date': date_str,
                'breakfast': data.get('breakfast', []),
                'lunch': data.get('lunch', []),
                'dinner': data.get('dinner', [])
            }
        except Exception as e:
            print(f"API에서 메뉴를 가져오는 중 오류 발생: {e}")
            return self._get_sample_menu(date_str)
    
    def _fetch_from_website(self, date_str: str) -> Dict[str, any]:
        """
        학교 홈페이지에서 메뉴를 크롤링합니다.
        AngularJS로 동적 생성되는 페이지이므로 Selenium을 사용합니다.
        """
        # ChromeDriverManager가 자동으로 Chrome을 감지하므로 별도 확인 불필요
        # Chrome이 없으면 ChromeDriverManager가 오류를 발생시킴
        
        driver = None
        try:
            # 1. Chrome 옵션 설정
            chrome_options = Options()
            
            # headless 모드 설정 (테스트할 때는 False로 설정하면 브라우저 창이 뜹니다)
            # 서버(GitHub Actions)에 올릴 때는 True로 설정해야 합니다
            if SELENIUM_HEADLESS:
                chrome_options.add_argument('--headless')
                print("🔧 Headless 모드 활성화 (브라우저 창이 뜨지 않습니다)")
            else:
                print("🔧 Headless 모드 비활성화 (브라우저 창이 뜹니다)")
            
            # 서버 환경에서도 안정적으로 동작하도록 추가 옵션
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
            
            # 2. ChromeDriver 자동 설치 및 설정
            # 운영체제에 따라 다르게 처리:
            # - Linux (GitHub Actions): 이미 설치된 Chrome 사용 (webdriver-manager 사용 안 함)
            # - Windows/Mac (로컬): webdriver-manager로 자동 설치
            print("🔍 ChromeDriver 설정 중...")
            try:
                if platform.system() == "Linux":
                    # 서버(GitHub Actions) 환경: 이미 설치된 Chrome을 사용
                    # browser-actions/setup-chrome이 Chrome과 ChromeDriver를 미리 설치해줌
                    print("   Linux 환경 감지: 설치된 Chrome 사용")
                    driver = webdriver.Chrome(options=chrome_options)
                    print("✅ ChromeDriver 설정 완료 (서버 환경)")
                else:
                    # 로컬 환경(Windows/Mac): webdriver-manager로 자동 설치
                    print("   로컬 환경 감지: ChromeDriver 자동 설치 중...")
                    service = Service(ChromeDriverManager().install())
                    driver = webdriver.Chrome(service=service, options=chrome_options)
                    print("✅ ChromeDriver 설정 완료 (로컬 환경)")
            except Exception as e:
                error_msg = f"❌ Chrome/ChromeDriver 설정 실패: {e}"
                print(error_msg)
                print("\n💡 해결 방법:")
                print("   1. Chrome 브라우저가 설치되어 있는지 확인하세요")
                print("   2. Windows: Chrome이 기본 설치 경로에 있는지 확인")
                print("   3. Ubuntu/Debian: sudo apt-get install google-chrome-stable")
                print("   4. macOS: brew install --cask google-chrome")
                raise RuntimeError(error_msg)
            
            # 3. 페이지 접속
            print(f"🌐 페이지 접속 중: {self.website_url}")
            driver.get(self.website_url)
            
            # 페이지 로딩 기다리기 (넉넉하게 3초)
            print("⏳ 페이지 로딩 대기 중...")
            time.sleep(3)
            
            # AngularJS가 메뉴를 로드할 때까지 대기 (최대 10초)
            wait = WebDriverWait(driver, 10)
            
            # 메뉴 컨테이너가 로드될 때까지 대기
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "nb-p-04-content")))
            
            # 추가로 JavaScript 실행 완료 대기 (2초)
            time.sleep(2)
            
            # 페이지 소스 가져오기
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            # 날짜 형식 변환 (YYYY-MM-DD -> YYYY.MM.DD)
            date_formatted = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y.%m.%d")
            
            # 현재 표시된 날짜 확인
            current_date_element = soup.select_one(".nb-p-time-select-current")
            if current_date_element:
                current_date = current_date_element.get_text(strip=True)
                print(f"현재 페이지 날짜: {current_date}, 요청 날짜: {date_formatted}")
            
            # 메뉴 추출 함수 (식당별로 구조화)
            def extract_menu_from_tab():
                """현재 활성화된 탭에서 식당별 메뉴를 추출"""
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                
                # 식당별 메뉴를 저장할 딕셔너리
                restaurant_menus = {}
                
                # 각 식당 (dl.nb-p-04-list-02)
                restaurant_elements = soup.select("dl.nb-p-04-list-02")
                
                for restaurant_elem in restaurant_elements:
                    # 식당 이름 추출 (dt 안의 span)
                    restaurant_name_elem = restaurant_elem.select_one("dt span.ng-binding")
                    if not restaurant_name_elem:
                        continue
                    restaurant_name = restaurant_name_elem.get_text(strip=True)
                    
                    # 해당 식당의 메뉴 코스들 (dd 요소들)
                    # ng-show로 숨겨진 것도 포함하여 모든 dd 요소 선택
                    menu_courses = []
                    course_elements = restaurant_elem.select("dd")
                    
                    # 디버깅: 식당 이름 출력
                    print(f"  식당 발견: {restaurant_name}, 코스 개수: {len(course_elements)}")
                    
                    # 식당이 접혀있을 수 있으므로 클릭하여 펼치기 시도
                    try:
                        # Selenium으로 dt 클릭하여 메뉴 펼치기
                        # XPath를 사용하여 식당 이름이 포함된 dt 요소 찾기
                        dt_xpath = f"//dl[@class='nb-p-04-list-02']//dt[.//span[contains(text(), '{restaurant_name}')]]"
                        dt_clickable = driver.find_element(By.XPATH, dt_xpath)
                        if dt_clickable:
                            dt_clickable.click()
                            time.sleep(0.5)  # 메뉴 펼쳐지는 시간 대기
                            # 다시 HTML 파싱
                            html = driver.page_source
                            soup = BeautifulSoup(html, 'html.parser')
                            # 해당 식당 요소 다시 찾기
                            restaurant_elems = soup.select("dl.nb-p-04-list-02")
                            for elem in restaurant_elems:
                                name_elem = elem.select_one("dt span.ng-binding")
                                if name_elem and restaurant_name in name_elem.get_text():
                                    restaurant_elem = elem
                                    course_elements = restaurant_elem.select("dd")
                                    break
                    except Exception as e:
                        print(f"  식당 펼치기 실패 (무시): {e}")
                    
                    for course_elem in course_elements:
                        # 코스 정보 추출
                        course_info = {}
                        
                        # 시간과 코스명
                        time_elem = course_elem.select_one(".meals-detail span.ng-binding")
                        if time_elem:
                            # 첫 번째 span은 시간, 두 번째는 코스명
                            spans = course_elem.select(".meals-detail span.ng-binding")
                            if len(spans) >= 2:
                                course_info['time'] = spans[0].get_text(strip=True)
                                course_info['course'] = spans[1].get_text(strip=True)
                            elif len(spans) == 1:
                                course_info['time'] = spans[0].get_text(strip=True)
                                course_info['course'] = ""
                        
                        # 메뉴 상세 (.nb-p-04-03 안의 p 태그들)
                        menu_detail_elem = course_elem.select_one(".nb-p-04-03")
                        if menu_detail_elem:
                            menu_items = menu_detail_elem.find_all('p')
                            course_info['menu'] = [item.get_text(strip=True) for item in menu_items if item.get_text(strip=True)]
                        else:
                            course_info['menu'] = []
                        
                        # 가격 (.meals-detail > div 안의 span에서 '원'이 포함된 것 찾기)
                        price_elem = None
                        # .meals-detail 안의 div에서 가격 span 찾기
                        meals_detail = course_elem.select_one(".meals-detail")
                        if meals_detail:
                            price_spans = meals_detail.select("span.ng-binding")
                            for span in price_spans:
                                text = span.get_text(strip=True)
                                if '원' in text:
                                    price_elem = span
                                    break
                        
                        if price_elem:
                            course_info['price'] = price_elem.get_text(strip=True)
                        else:
                            course_info['price'] = ""
                        
                        if course_info.get('menu'):  # 메뉴가 있는 경우만 추가
                            menu_courses.append(course_info)
                    
                    if menu_courses:
                        restaurant_menus[restaurant_name] = menu_courses
                
                return restaurant_menus
            
            # 조식/중식/석식 탭을 각각 클릭하여 메뉴 추출
            breakfast_menu = {}
            lunch_menu = {}
            dinner_menu = {}
            
            # 4. 버튼/탭 클릭하여 메뉴 가져오기
            # F12를 눌러서 개발자 도구에서 버튼의 selector를 찾아야 합니다
            # 예: id가 'today-btn'인 경우 -> By.ID, "today-btn"
            # 예: class가 'lunch'인 경우 -> By.CSS_SELECTOR, ".lunch"
            # 예: 텍스트가 '중식'인 경우 -> By.XPATH, "//em[contains(text(), '중식')]"
            
            try:
                # 조식 탭 클릭
                print("🔘 조식 탭 클릭 중...")
                # XPath를 사용하여 '조식' 텍스트가 포함된 em 태그 찾기
                breakfast_tab = wait.until(EC.presence_of_element_located((By.XPATH, "//em[contains(text(), '조식')]")))
                if breakfast_tab:
                    # JavaScript로 클릭 (더 안정적)
                    driver.execute_script("arguments[0].click();", breakfast_tab)
                    time.sleep(1.5)  # 메뉴 로딩 대기
                    breakfast_menu = extract_menu_from_tab()
                    total_courses = sum(len(courses) for courses in breakfast_menu.values())
                    print(f"✅ 조식 메뉴: {len(breakfast_menu)}개 식당, {total_courses}개 코스")
            except (TimeoutException, NoSuchElementException, AttributeError) as e:
                print(f"⚠️  조식 탭을 찾을 수 없습니다: {e}")
                print("   F12를 눌러서 개발자 도구에서 조식 버튼의 selector를 확인하세요")
            
            try:
                # 중식 탭 클릭
                print("🔘 중식 탭 클릭 중...")
                # XPath를 사용하여 '중식' 텍스트가 포함된 em 태그 찾기
                lunch_tab = wait.until(EC.presence_of_element_located((By.XPATH, "//em[contains(text(), '중식')]")))
                if lunch_tab:
                    # JavaScript로 클릭 (더 안정적)
                    driver.execute_script("arguments[0].click();", lunch_tab)
                    time.sleep(1.5)  # 메뉴 로딩 대기
                    lunch_menu = extract_menu_from_tab()
                    total_courses = sum(len(courses) for courses in lunch_menu.values())
                    print(f"✅ 중식 메뉴: {len(lunch_menu)}개 식당, {total_courses}개 코스")
            except (TimeoutException, NoSuchElementException, AttributeError) as e:
                print(f"⚠️  중식 탭을 찾을 수 없습니다: {e}")
                print("   F12를 눌러서 개발자 도구에서 중식 버튼의 selector를 확인하세요")
            
            try:
                # 석식 탭 클릭
                print("🔘 석식 탭 클릭 중...")
                # XPath를 사용하여 '석식' 텍스트가 포함된 em 태그 찾기
                dinner_tab = wait.until(EC.presence_of_element_located((By.XPATH, "//em[contains(text(), '석식')]")))
                if dinner_tab:
                    # JavaScript로 클릭 (더 안정적)
                    driver.execute_script("arguments[0].click();", dinner_tab)
                    time.sleep(1.5)  # 메뉴 로딩 대기
                    dinner_menu = extract_menu_from_tab()
                    total_courses = sum(len(courses) for courses in dinner_menu.values())
                    print(f"✅ 석식 메뉴: {len(dinner_menu)}개 식당, {total_courses}개 코스")
            except (TimeoutException, NoSuchElementException, AttributeError) as e:
                print(f"⚠️  석식 탭을 찾을 수 없습니다: {e}")
                print("   F12를 눌러서 개발자 도구에서 석식 버튼의 selector를 확인하세요")
            
            # 메뉴가 하나도 없으면 기본적으로 중식 탭의 메뉴를 가져옴
            if not breakfast_menu and not lunch_menu and not dinner_menu:
                print("⚠️  탭 클릭으로 메뉴를 가져올 수 없어 기본 방법으로 시도합니다.")
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                # 기본적으로 중식 탭이 활성화되어 있으므로 중식 메뉴 추출
                lunch_menu = extract_menu_from_tab()
            
            # 메뉴가 없으면 에러 발생
            if not breakfast_menu and not lunch_menu and not dinner_menu:
                error_msg = "❌ 메뉴를 찾을 수 없습니다. 크롤링에 실패했습니다."
                print(error_msg)
                raise RuntimeError(error_msg)
            
            total_restaurants = len(set(list(breakfast_menu.keys()) + list(lunch_menu.keys()) + list(dinner_menu.keys())))
            print(f"✅ 메뉴 추출 완료 - 총 {total_restaurants}개 식당")
            
            return {
                'date': date_str,
                'breakfast': breakfast_menu,
                'lunch': lunch_menu,
                'dinner': dinner_menu
            }
            
        except TimeoutException:
            error_msg = "❌ 페이지 로딩 시간 초과. 크롤링에 실패했습니다."
            print(error_msg)
            raise RuntimeError(error_msg)
        except Exception as e:
            error_msg = f"❌ 웹사이트에서 메뉴를 가져오는 중 오류 발생: {e}"
            print(error_msg)
            import traceback
            traceback.print_exc()
            raise RuntimeError(error_msg)
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass  # 이미 종료된 경우 무시
    
    def _get_sample_menu(self, date_str: str) -> Dict[str, any]:
        """
        샘플 메뉴 데이터를 반환합니다.
        실제 사용 시에는 학교 급식 API로 교체해야 합니다.
        """
        # 요일별 샘플 메뉴
        weekday = datetime.strptime(date_str, "%Y-%m-%d").weekday()
        sample_menus = [
            {
                'breakfast': ['밥', '된장국', '계란후라이', '김치', '요구르트'],
                'lunch': ['밥', '김치찌개', '제육볶음', '시금치나물', '배추김치', '수정과'],
                'dinner': ['밥', '미역국', '돈까스', '콩나물무침', '깍두기']
            },
            {
                'breakfast': ['밥', '미역국', '어묵볶음', '단무지', '우유'],
                'lunch': ['밥', '된장찌개', '치킨너겟', '시금치나물', '배추김치', '요구르트'],
                'dinner': ['밥', '계란국', '불고기', '콩나물무침', '깍두기']
            },
            {
                'breakfast': ['밥', '계란국', '소시지', '단무지', '우유'],
                'lunch': ['밥', '순두부찌개', '닭볶음탕', '시금치나물', '배추김치', '수정과'],
                'dinner': ['밥', '된장국', '제육볶음', '콩나물무침', '깍두기']
            },
            {
                'breakfast': ['밥', '된장국', '계란후라이', '김치', '요구르트'],
                'lunch': ['밥', '김치찌개', '돈까스', '시금치나물', '배추김치', '수정과'],
                'dinner': ['밥', '미역국', '불고기', '콩나물무침', '깍두기']
            },
            {
                'breakfast': ['밥', '미역국', '어묵볶음', '단무지', '우유'],
                'lunch': ['밥', '된장찌개', '치킨너겟', '시금치나물', '배추김치', '요구르트'],
                'dinner': ['밥', '계란국', '제육볶음', '콩나물무침', '깍두기']
            },
            {
                'breakfast': ['밥', '계란국', '소시지', '단무지', '우유'],
                'lunch': ['밥', '순두부찌개', '닭볶음탕', '시금치나물', '배추김치', '수정과'],
                'dinner': ['밥', '된장국', '돈까스', '콩나물무침', '깍두기']
            },
            {
                'breakfast': ['밥', '된장국', '계란후라이', '김치', '요구르트'],
                'lunch': ['밥', '김치찌개', '제육볶음', '시금치나물', '배추김치', '수정과'],
                'dinner': ['밥', '미역국', '불고기', '콩나물무침', '깍두기']
            }
        ]
        
        menu = sample_menus[weekday]
        # 샘플 데이터도 식당별로 구조화 (실제 학교 식당 구조 반영)
        return {
            'date': date_str,
            'breakfast': {
                '참슬기식당(310관 B4층)': [{
                    'time': '07:00~09:00',
                    'course': '조식',
                    'menu': menu['breakfast'],
                    'price': '3,500 원'
                }]
            },
            'lunch': {
                '카우잇츠(cau eats)': [
                    {
                        'time': '11:30~14:00',
                        'course': '중식(특식)',
                        'menu': ['김치국', '찹스테이크', '생선까스*타르소스', '파래자반', '파인애플', '깍두기'],
                        'price': '5,500 원'
                    },
                    {
                        'time': '11:30~14:00',
                        'course': '중식(일품1)',
                        'menu': ['떡만두국', '김치'],
                        'price': '4,000 원'
                    },
                    {
                        'time': '11:30~14:00',
                        'course': '중식(일품2)',
                        'menu': ['비빔칼국수', '대패삼겹구이', '단무지'],
                        'price': '4,000 원'
                    }
                ],
                '(다빈치)라면': [{
                    'time': '11:00~16:00',
                    'course': '중식(중식)',
                    'menu': ['신라면', '너구리', '진라면매운맛', '안성탕면'],
                    'price': '2,500 원'
                }],
                '참슬기식당(310관 B4층)': [
                    {
                        'time': '11:00~13:30',
                        'course': '중식(한식)',
                        'menu': ['육개장칼국수', '찐만두', '무말랭이지'],
                        'price': '4,000 원'
                    },
                    {
                        'time': '11:30~13:30',
                        'course': '중식(특식)',
                        'menu': ['사천짜장덮밥', '계란부추국', '유린기', '감자샐러드', '김치'],
                        'price': '5,500 원'
                    }
                ],
                '생활관식당(블루미르308관)': [{
                    'time': '11:30~13:30',
                    'course': '중식',
                    'menu': menu['lunch'],
                    'price': '4,500 원'
                }],
                '학생식당(303관B1층)': [{
                    'time': '11:30~14:00',
                    'course': '중식',
                    'menu': menu['lunch'],
                    'price': '4,000 원'
                }]
            },
            'dinner': {
                '참슬기식당(310관 B4층)': [{
                    'time': '17:30~19:00',
                    'course': '석식',
                    'menu': menu['dinner'],
                    'price': '4,500 원'
                }],
                '생활관식당(블루미르308관)': [{
                    'time': '17:30~19:00',
                    'course': '석식',
                    'menu': menu['dinner'],
                    'price': '4,500 원'
                }]
            }
        }
    
    def format_menu_message(self, menu_data: Dict[str, any]) -> str:
        """
        메뉴 데이터를 Slack 메시지 형식으로 포맷팅합니다.
        간결하고 읽기 쉬운 형식으로 표시합니다.
        
        Args:
            menu_data: 메뉴 정보 딕셔너리
            
        Returns:
            str: 포맷팅된 메시지
        """
        date = menu_data['date']
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        weekday_kr = ['월', '화', '수', '목', '금', '토', '일']
        weekday = weekday_kr[date_obj.weekday()]
        month_day = date_obj.strftime("%m/%d")
        
        message = f"📅 {month_day}({weekday}) 오늘의 급식\n\n"
        
        # 식당 이름을 간단하게 변환하는 함수
        def simplify_restaurant_name(name: str) -> str:
            """식당 이름을 간단하게 변환"""
            # 308관, 309관, 310관, 303관 등 추출
            if '308관' in name or '블루미르308관' in name:
                return '308관'
            elif '309관' in name or '블루미르309관' in name:
                return '309관'
            elif '310관' in name or 'B4층' in name:
                return '310관 B4'
            elif '303관' in name or 'B1층' in name:
                return '303관 B1'
            elif '102관' in name or 'University Club' in name:
                return '102관'
            return name
        
        # 코스명 정리 함수
        def clean_course_name(course_name: str) -> str:
            """코스명을 간단하게 정리"""
            if not course_name:
                return ""
            # 괄호 제거 및 정리
            course = course_name.replace('조식(', '').replace('중식(', '').replace('석식(', '').replace(')', '')
            # 불필요한 단어 제거
            if course in ['조식', '중식', '석식', '한식']:
                return ""
            return course
        
        # 조식 포맷팅
        breakfast_found = False
        breakfast_times = []
        if menu_data.get('breakfast'):
            if isinstance(menu_data['breakfast'], dict):
                # 시간 범위 추출
                for courses in menu_data['breakfast'].values():
                    for course in courses:
                        if course.get('time'):
                            breakfast_times.append(course['time'])
                
                time_range = ""
                if breakfast_times:
                    start_times = []
                    end_times = []
                    for time_str in breakfast_times:
                        if '~' in time_str:
                            parts = time_str.split('~')
                            start_times.append(parts[0])
                            end_times.append(parts[1])
                    if start_times and end_times:
                        time_range = f"({min(start_times)}~{max(end_times)})"
                
                message += f"*🌅 조식{(' ' + time_range) if time_range else ''}*\n"
                
                for restaurant_name, courses in menu_data['breakfast'].items():
                    if not courses:
                        continue
                    
                    for course in courses:
                        menu_items = course.get('menu', [])
                        if not menu_items:
                            continue
                        
                        breakfast_found = True
                        simple_name = simplify_restaurant_name(restaurant_name)
                        price_str = course.get('price', '').replace(' 원', '원')
                        menu_text = " · ".join(menu_items)
                        message += f"- {simple_name} ({price_str}원) : {menu_text}\n"
                
                if not breakfast_found:
                    message += "- (메뉴 없음)\n"
                message += "\n"
        
        # 중식 포맷팅
        lunch_found = False
        lunch_times = []
        if menu_data.get('lunch'):
            if isinstance(menu_data['lunch'], dict):
                # 시간 범위 추출
                for courses in menu_data['lunch'].values():
                    for course in courses:
                        if course.get('time'):
                            lunch_times.append(course['time'])
                
                time_range = ""
                if lunch_times:
                    start_times = []
                    end_times = []
                    for time_str in lunch_times:
                        if '~' in time_str:
                            parts = time_str.split('~')
                            start_times.append(parts[0])
                            end_times.append(parts[1])
                    if start_times and end_times:
                        time_range = f"({min(start_times)}~{max(end_times)})"
                
                message += f"*🍴 중식{(' ' + time_range) if time_range else ''}*\n"
                
                for restaurant_name, courses in menu_data['lunch'].items():
                    if not courses:
                        continue
                    simple_name = simplify_restaurant_name(restaurant_name)
                    
                    for course in courses:
                        menu_items = course.get('menu', [])
                        if not menu_items:
                            continue
                        
                        lunch_found = True
                        course_name = clean_course_name(course.get('course', ''))
                        price_str = course.get('price', '').replace(' 원', '원')
                        menu_text = " · ".join(menu_items)
                        
                        # 코스명이 있으면 앞에 추가
                        course_prefix = f"{course_name} " if course_name else ""
                        message += f"- {simple_name} ({price_str}원) : {course_prefix}{menu_text}\n"
                
                if not lunch_found:
                    message += "- (메뉴 없음)\n"
                message += "\n"
        
        # 석식 포맷팅
        dinner_found = False
        dinner_times = []
        if menu_data.get('dinner'):
            if isinstance(menu_data['dinner'], dict):
                # 시간 범위 추출
                for courses in menu_data['dinner'].values():
                    for course in courses:
                        if course.get('time'):
                            dinner_times.append(course['time'])
                
                time_range = ""
                if dinner_times:
                    start_times = []
                    end_times = []
                    for time_str in dinner_times:
                        if '~' in time_str:
                            parts = time_str.split('~')
                            start_times.append(parts[0])
                            end_times.append(parts[1])
                    if start_times and end_times:
                        time_range = f"({min(start_times)}~{max(end_times)})"
                
                message += f"*🌙 석식{(' ' + time_range) if time_range else ''}*\n"
                
                for restaurant_name, courses in menu_data['dinner'].items():
                    if not courses:
                        continue
                    simple_name = simplify_restaurant_name(restaurant_name)
                    
                    for course in courses:
                        menu_items = course.get('menu', [])
                        if not menu_items:
                            continue
                        
                        dinner_found = True
                        course_name = clean_course_name(course.get('course', ''))
                        price_str = course.get('price', '').replace(' 원', '원')
                        menu_text = " · ".join(menu_items)
                        
                        # 코스명이 있으면 앞에 추가
                        course_prefix = f"{course_name} " if course_name else ""
                        message += f"- {simple_name} ({price_str}원) : {course_prefix}{menu_text}\n"
                
                if not dinner_found:
                    message += "- (메뉴 없음)\n"
        
        # 모든 메뉴가 없으면 안내 메시지
        if not breakfast_found and not lunch_found and not dinner_found:
            message += "\n⚠️ 해당 날짜의 메뉴 정보가 없습니다."
        
        return message

