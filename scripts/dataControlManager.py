from newV_GetJumpitPageHTML import PageCrawler

pageCrawler = PageCrawler("C:\\Users\\soldesk\\Downloads\\chrome-win64\\chrome-win64\\chrome.exe")

# soup = pageCrawler.load_JobsAllData(url="https://jumpit.saramin.co.kr/positions?sort=rsp_rate", max_scrolls=1)

# url_list = pageCrawler.extract_JobLinks(soup, max_website_count=3)
# print(url_list)
# for link in url_list:
#     print(link)
#     print(pageCrawler.parse_JobDetail(link))

# # 셀레니움 웹 드라이버 임포트 해 주기
# from selenium import webdriver

# # Chrome 웹 드라이버 경로
# driver_path = "C:\\Users\\soldesk\\Downloads\\chrome-win64\\chrome-win64\\chrome.exe"

# # Chrome 브라우저 열기
# driver = webdriver.Chrome()

# # 구글 페이지 연결시키기
# driver.get("https://google.com")

print(pageCrawler.parse_JobDetail("https://jumpit.saramin.co.kr/position/49621"))
print(pageCrawler.parse_JobDetail("https://jumpit.saramin.co.kr/position/49729"))