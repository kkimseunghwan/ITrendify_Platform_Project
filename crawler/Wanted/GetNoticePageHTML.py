from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time


# executable_path="C:/Users/rhian/Downloads/chromedriver-win64/chromedriver.exe"
# url = "https://www.wanted.co.kr/wdlist/518"
class PageCrawler:
    # 생성자. : 초기 연결 및 기타 설정
    def __init__(self, driver_path):
        # ** executable_path 경로 설정을 위한 환경 변수 설정 필요 **
        service = Service(executable_path=driver_path) 
        self.driver = webdriver.Chrome(service=service)
        self.base_url = "https://www.wanted.co.kr"

        self.job_roles = {
            872: "서버 개발자",
            10110: "소프트웨어 엔지니어",
            660: "자바 개발자",
            669: "프론트엔드 개발자",
            873: "웹 개발자",
            899: "파이썬 개발자",
            900: "C, C++ 개발자",
            1634: "머신러닝 엔지니어",
            655: "데이터 엔지니어",
            665: "시스템 관리자",
            677: "안드로이드 개발자",
            895: "Node.js 개발자",
            676: "QA 엔지니어",
            1024: "데이터 사이언티스트",
            658: "임베디드 개발자",
            1025: "빅데이터 엔지니어",
            678: "IOS 개발자"
        }

        self.section_titles = ["주요업무", "자격요건", "우대사항"] # 저장할 데이터 종류 중 일부 리스트 저장
    
    def close(self):
        self.driver.quit()

    
    # 직군 전체로 해서 공고ID가 담긴 페이지 HTML 반환할떄 사용
    def load_JobsAll(self, url, role_id=None, max_scrolls=20, pause_time=1):
        
        # role_id가 주어지면 해당 직무만 크롤링
        if role_id is not None:
            url += f"/{role_id}"  # 특정 직무만 나오도록 대상 사이트 변경

        # 공고 리스트 페이지 이동
        self.driver.get(url)
        # 페이지 로딩 대기
        time.sleep(2)

        
        # 원티드 페이지 자체가 아래쪽으로 스크롤 해야 목록이 더 나오는 형식이라
        # 데이터를 더 모으기 위해서는 페이지를 알아서 스크롤 하게 해야됨.

        # 초기 페이지 높이 저장
        last_height = self.driver.execute_script("return document.body.scrollHeight") 

        # 페이지를 끝까지 내리기 or 최대 횟수 만큼 내리기
        for count in range(max_scrolls):
            # 페이지 맨 아래로 스크롤 : JS명령어
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            time.sleep(pause_time)

            # 스크롤 후 페이지 전체 높이
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            
            if new_height == last_height:
                print(f"공고 더 없음. {count}회 스크롤 함. 종료.")
                break
            
            # 페이지 높이 업데이트
            last_height = new_height
            
        # HTML 가져와서 읽어서 반환
        return BeautifulSoup(self.driver.page_source, 'html.parser')
    
    # HTML에서 공고들의 ID가 포함된 a태그의 data-attribute-id 들을 찾기.
    def extract_JobLinks(self, soup:BeautifulSoup):
        # 공고 주소 형태 : https://www.wanted.co.kr/wd/237131
        # HTML에서 공고들의 ID가 포함된 a태그의 data-attribute-id 들을 찾아서 리스트화.
        return [self.base_url + a.get('href') for a in soup.find_all("a", {"data-attribute-id": "position__click"}) if a.get('href')]

    
    # 공고 페이지 내부 데이터 모두 조회.
    def parse_JobDetail(self, job_url, job_roleId=None):
        try:
            # 공고 페이지 접속
            self.driver.get(job_url)

            # 페이지 로딩 대기.
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'wds-1y0suvb'))
            )
            
            # 우대사항하고 공고 모든 내용이 상세 정보 더보기 버튼을 눌러야 보임
            # 상세 정보 더보기 버튼이 있으면 클릭 시도
            try:
                more_info_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='상세 정보 더 보기']]"))
                )
                self.driver.execute_script("arguments[0].click();", more_info_button)  # JavaScript로 강제 클릭
                time.sleep(1)  # 클릭 후 로딩 대기
            except:
                # 버튼이 없거나 클릭이 불가능할때
                pass

            # 다시 HTML 파싱
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # 기본 정보 추출
            company_name = soup.find('strong', class_='CompanyInfo_CompanyInfo__name__sBeI6')
            title = soup.find('h1', class_='wds-jtr30u')

            info_spans = soup.find_all('span', class_='JobHeader_JobHeader__Tools__Company__Info__b9P4Y wds-rgovpd')
            location = info_spans[0].text if len(info_spans) > 0 else None
            career = info_spans[-1].text if len(info_spans) > 1 else None      

            # 비정형 데이터들 추출 : 주요업무, 자격요건, 우대사항
            sections = {key: None for key in self.section_titles}
            for h3 in soup.find_all('h3', class_='wds-1y0suvb'):
                data = h3.text.strip()
                if data in sections:
                    span = h3.find_parent('div').find('span', class_='wds-wcfcu3')
                    if span: sections[data] = span.get_text(separator="\n")

            return {
                "url": job_url,
                "회사명": company_name.text if company_name else None,
                "제목": title.text if title else None,
                "지역": location,
                "경력": career,
                "주요업무": sections["주요업무"],
                "자격요건": sections["자격요건"],
                "우대사항": sections["우대사항"],
                "직무ID":job_roleId
            }

        except Exception as e:
            print(f"[오류 발생] {e}")
            return None







