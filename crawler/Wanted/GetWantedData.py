
from GetNoticePageHTML import PageCrawler

# executable_path="C:/Users/rhian/Downloads/chromedriver-win64/chromedriver.exe"
# url = "https://www.wanted.co.kr/wdlist/518"

if __name__ == "__main__":
    executable_path="C:/Users/rhian/Downloads/chromedriver-win64/chromedriver.exe"
    crawler = PageCrawler(executable_path) # 생성자 생성, 크롬 연결

    try:
        for role_id, role_name in crawler.job_roles.items():
            soup = crawler.load_JobsAll("https://www.wanted.co.kr/wdlist/518", role_id, max_scrolls=1)
            job_links = crawler.extract_JobLinks(soup)

            print("======================", role_name, "======================")
            for url in job_links:
                data = crawler.parse_JobDetail(url, role_id) 
                if data:
                    print("=" * 40)
                    for k, v in data.items():
                        print(f"{k}:\n{v}\n")

    finally:
        crawler.close()


