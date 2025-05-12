# 원본 데이터 객체
class OriginData:
    def __init__(self, id, url, company, title, tech_stack, location, career, education, type, 
                 main_task, qualification, benefits, 
                 write_date, deadline):
        
        # 원본 데이터 객체 초기화
        self.id = id                        # 고유 아이디
        self.url = url                      # 웹사이트 주소
        self.company = company              # 회사명
        self.title = title                  # 공고제목
        self.tech_stack = tech_stack        # 기술 스택
        self.location = location            # 근무지역
        self.career = career                # 경력
        self.education = education          # 학력
        self.type = type                    # 직무 분류
        self.main_task = main_task          # 주요 업무
        self.qualification = qualification  # 자격 조건
        self.benefits = benefits            # 우대 사항 
        self.write_date = write_date        # 등록 날짜
        self.deadline = deadline            # 마감일


'''
DVA 형식 구조 계획
'''