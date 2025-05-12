# <script> 안의 JSON 데이터 파싱
# 굳이 HTML 파싱 필요 없음
# script 태그 안의 JSON 데이터에 HTML에 전달할 모든 데이터가 포함되어 있음

import re
import json
from bs4 import BeautifulSoup

class JsonCrawler:
    # 생성자 : 초기 연결 및 기타 설정
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')
        self.parsed_data = self._search_for_valid_data()

    def _search_json_in_push_array(self):
        scripts = self.soup.find_all('script')
        for i, script in enumerate(scripts):
            text = script.text
            if '__next_f.push' not in text:
                continue

            # self.__next_f.push([...]) 안의 내용 추출
            push_matches = re.findall(r'self\.__next_f\.push\(\[(.*?)\]\)', text, re.DOTALL)
            for match in push_matches:
                # 문자열 안에 JSON 구조가 있으면 시도
                try:
                    # 강제 JSON 배열 형태로 만들기 위한 처리
                    possible_json = "[" + match + "]"
                    json_array = json.loads(possible_json)

                    for obj in json_array:
                        if isinstance(obj, dict) and "data" in obj:
                            data = obj["data"]
                            if "title" in data and "companyName" in data:
                                print(f"[DEBUG] script #{i} - JSON 객체 내부에서 유효한 공고 발견됨")
                                return self._extract_fields(data)

                except json.JSONDecodeError:
                    continue

        print("[DEBUG] 모든 <script> 검사 완료 → 유효한 JSON 데이터 없음")
        return {}


    def _extract_fields(self, data):
        return {
            "id": data.get("id"),
            "title": data.get("title"),
            "company": data.get("companyName"),
            "tech_stacks": [s["stack"] for s in data.get("techStacks", [])],
            "responsibilities": data.get("responsibility"),
            "qualifications": data.get("qualifications"),
            "preferred": data.get("preferredRequirements"),
            "welfare": data.get("welfares"),
            "location": data.get("workingPlaces", [{}])[0].get("address"),
            "categories": [c["name"] for c in data.get("jobCategories", [])],
            "deadline": data.get("closedAt"),
            "url": f"https://www.jumpit.co.kr/position/{data.get('id')}"
        }

    def get_parsed_data(self):
        return self.parsed_data