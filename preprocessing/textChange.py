

# 경력 텍스트 변환
# -> career_min, career_max 두 개로 저장.
def carrerPreProcessing(text):
    carrer_min = None
    carrer_max = None
    try:
        if text == '신입':
            return 0, 0
        elif text == '무관':
            return None, None
        elif '~' in text:
            text = text.split('~')

            if text[0] == "신입":
                carrer_min = 0
            else:
                carrer_min = int(text[0].replace("경력", "").strip())

            carrer_max = int(text[1].replace('년', ''))
            
            return carrer_min, carrer_max
        else:
            return None, None
    except Exception as e:
        print(text, e)
        return None, None


# 지역 텍스트 전처리
# -> 하나로
# ex)
# 무관 -> 무관
# 서울 강남구 학동로 402 천마빌딩 5층 -> 서울시 강남구
# 서울 서초구 매헌로8길 39 2층(양재동,희경재단) -> 서울시 서초구
# 경기 용인시 수지구 신수로 767 분당수지유타워 A동 1001호 -> 용인시 수지구
def locationPreProcessing(text):
    location = None
    try:
        if text == '무관':
            return '무관'
        else:
            return text
    except Exception as e:
        print(text, e)
        return None

a = '경력 9~20년'
b = '신입~2년'
c = '신입'
print(carrerPreProcessing(a))
print(carrerPreProcessing(b))
print(carrerPreProcessing(c))


