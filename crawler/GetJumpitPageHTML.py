from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time

# executable_path="C:/Users/rhian/Downloads/chromedriver-win64/chromedriver.exe"
# url = https://jumpit.saramin.co.kr/positions?sort=reg_dt

# 응답률순(기본값) : https://jumpit.saramin.co.kr/positions?sort=rsp_rate
# 최신순 : https://jumpit.saramin.co.kr/positions?sort=reg_dt
# 인기순 : https://jumpit.saramin.co.kr/positions?sort=popular

class PageCrawler:
    # 생성자 init : 초기 연결 및 기타 설정
    def __init__(self, driver_path):
        service = Service(executable_path=driver_path)
        self.driver = webdriver.Chrome()
        self.base_url = "https://jumpit.saramin.co.kr"

        # 저장할 데이터 종류 중 일부 리스트 저장
        self.section_titles = ["주요업무", "자격요건", "우대사항"]

    def close(self):
        self.driver.quit()

    # 공고 리스트 페이지 크롤링
    def load_JobsAllData(self, url="https://jumpit.saramin.co.kr/positions?sort=rsp_rate", max_scrolls=5, pause_time=1):
        self.driver.get(url)
        time.sleep(2)

        if "jobCategory=" in url:
            print("개발 직무 선택됨")

        last_height = self.driver.execute_script("return document.body.scrollHeight")

        for count in range(max_scrolls):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(pause_time)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print(f"스크롤 {count}회. 종료.")
                break
            last_height = new_height

        soap = BeautifulSoup(self.driver.page_source, 'html.parser')
        return soap

    # 공고 URL 추출
    def extract_JobLinks(self, soup: BeautifulSoup, max_website_count=10):
        url_list = []
        for a in soup.select("div[class^='sc-d609d44f-0'] a"):
            if len(url_list) >= max_website_count:
                break
            if a.get('href'):
                url_list.append(self.base_url + a['href'])

        return url_list

    # 상세 공고 내용 크롤링
    def parse_JobDetail(self, job_url, pause_time=1):
        try:
            self.driver.get(job_url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            )
            # 서버 부하 방지를 위해 일정 시간 대기
            time.sleep(pause_time)

            # HTML 파싱
            soup = BeautifulSoup(self.driver.page_source, "html.parser")

            # 공고 ID 추출
            job_id = int(job_url.split("/")[-1])

            # 공고 제목
            title_div = soup.find("div", class_="sc-923c3317-0 jIWuEG")
            title = title_div.find("h1")
            # 회사 이름
            company = title_div.find("a", class_="name").find("span")

            # 기술 스택 리스트
            tech_stack_list = [ div.find("img")["alt"] for div in soup.select("pre div", class_="sc-e76d2562-1 eALIki") ]
            
            # 경력, 지역, 학력, 마감일 정보 추출   
            etc_info = soup.find("div", class_="sc-b12ae455-0 ehVsnD")
            career = etc_info.find('dt', string='경력').find_next('dd').text.strip()
            location = etc_info.find('dt', string='근무지역').find_next('dd').find('li').text.strip().replace("지도보기·주소복사", "")
            education = etc_info.find('dt', string='학력').find_next('dd').text.strip()
            deadline = etc_info.find('dt', string='마감일').find_next('dd').text.strip()
            
            # 코드 돌리는 시간
            write_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 주요업무, 자격요건, 우대사항 정보 추출
            sections = {key: None for key in self.section_titles}

            for dl in soup.find_all("dl", class_="sc-e76d2562-0 jqzywl"):
                dt = dl.find("dt") # 형식 분류
                dd = dl.find("dd") # 내부 내용 
                if dt and dt.text.strip() in sections:
                    sections[dt.text.strip()] = dd.get_text(separator="\n").strip() # 내부 내용을 \n 으로 구분

            # 딕셔너리 형식으로 반환
            return {
                "id": job_id,
                "url": job_url,
                "회사명": company.text.strip() if company else None,
                "제목": title.text.strip() if title else None,
                "지역": location,
                "경력": career,
                "학력": education,
                "기술스택": tech_stack_list,
                "주요업무": sections["주요업무"],
                "자격요건": sections["자격요건"],
                "우대사항": sections["우대사항"],
                "등록일": write_date,
                "마감일": deadline
            }

        except Exception as e:
            print(f"[오류] {e}")
            return None
