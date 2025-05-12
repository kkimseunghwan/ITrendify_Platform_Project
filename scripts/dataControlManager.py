
# 스크립트의 상위 폴더(루트 폴더)를 찾아서 경로 추가
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 크롤러 파일 임포트
from crawler.GetJumpitPageHTML import PageCrawler
from crawler.GetJumpitPageScript import JsonCrawler
from database.OriginData import OriginData


# 데이터 제어 관리자 클래스
if __name__ == "__main__":
    pageCrawler = PageCrawler()

    soup = pageCrawler.load_JobsAllData(url="https://jumpit.saramin.co.kr/positions?sort=rsp_rate", max_scrolls=1)
    
    url_list = pageCrawler.extract_JobLinks(soup, max_website_count=1) # 테스트용 2개
    print(url_list)

    for link in url_list:
        # 개별 공고 HTML 가져오기
        pageCrawler.driver.get(link)
        html = pageCrawler.driver.page_source

        # 파서 객체로 JSON 파싱
        parser = JsonCrawler(html)
        print(parser.get_parsed_data())

        # 데이터 출력 (또는 DB 저장 등)
        # if pageData:
        #     print("[성공] 추출된 데이터:")
        #     for k, v in pageData.items():
        #         print(f"{k}: {v}")

        # print(link)
        # pageData = pageCrawler.parse_JobDetail(link)

        # id = pageData.get("id")
        # url = pageData.get("url")
        # company = pageData.get("회사명")
        # title = pageData.get("제목")
        # tech_stack = pageData.get("기술스택")
        # location = pageData.get("지역")
        # career = pageData.get("경력")
        # education = pageData.get("학력")
        # type = pageData.get("직무분류")
        # main_task = pageData.get("주요업무")
        # qualification = pageData.get("자격요건")
        # benefits = pageData.get("우대사항")
        # write_date = pageData.get("등록일")
        # deadline = pageData.get("마감일")
        

        # originDataDAO = OriginData()


    # 웹사이트 반환값 테스트
    # print(pageCrawler.parse_JobDetail("https://jumpit.saramin.co.kr/position/49621"))
    # print(pageCrawler.parse_JobDetail("https://jumpit.saramin.co.kr/position/49729"))
