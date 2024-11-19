import requests
from config import MOVIE_API_KEY
from datetime import datetime, timedelta

def getDailyBoxOffice():
    # API 기본 URL 및 인증키
    BASE_URL = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList"

    # 오늘 날짜 가져오기
    today = datetime.today()

    # 어제 날짜 계산
    yesterday = today - timedelta(days=1)

    # yyyymmdd 형식으로 변환
    formatted_date = yesterday.strftime("%Y%m%d")

    # 요청 파라미터
    params = {
        "key": MOVIE_API_KEY,
        "targetDt": formatted_date,  # 검색할 영화 이름
        "itemPerPage": "1"
    }

    # JSON 형식으로 요청
    response = requests.get(f"{BASE_URL}.json", params=params)

    # 응답 데이터 확인
    if response.status_code == 200:
        data = response.json()
        movie_list = []
        for movie in data["boxOfficeResult"]["dailyBoxOfficeList"]:
            movie_list.append([movie["movieNm"], movie["openDt"], movie["audiAcc"]])
        
        return movie_list
    else:
        print(f"일일 박스오피스 요청 실패: {response.status_code}")
        return -1

def getWeeklyBoxOffice():
    # API 기본 URL 및 인증키
    BASE_URL = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList"

    # 오늘 날짜 가져오기
    today = datetime.today()

    # 오늘이 속한 주의 월요일 날짜 계산
    first_day_of_month = today.replace(day=1)
    first_day_of_month = first_day_of_month.strftime("%Y%m%d")

    # 요청 파라미터 설정
    params = {
        "key": MOVIE_API_KEY,
        "targetDt": first_day_of_month,  # 조회할 날짜 (yyyymmdd 형식)
        "weekGb": "0",          # 주말: "1" (default), 주간: "0", 주중: "2"
        "itemPerPage": "1",    # 결과 개수
        "multiMovieYn": "N",    # 상업영화만 조회 ("Y" : 다양성 영화, "N" : 상업영화)
        "repNationCd": "K",     # 한국 영화만 조회 ("K" : 한국, "F" : 외국)
        "wideAreaCd": ""        # 상영 지역 (default: 전체)
    }

    # JSON 형식으로 요청
    response = requests.get(f"{BASE_URL}.json", params=params)

    # 응답 데이터 확인
    if response.status_code == 200:
        data = response.json()
        movie_list = []
        for movie in data["boxOfficeResult"]["weeklyBoxOfficeList"]:
            movie_list.append([movie["movieNm"], movie["openDt"], movie["audiAcc"]])
        
        return movie_list
    else:
        print(f"주간 박스오피스 요청 실패: {response.status_code}")
        return -1
    

