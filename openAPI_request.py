import requests
from config import MOVIE_API_KEY

# API 기본 URL 및 인증키
BASE_URL = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList"

# 요청 파라미터
params = {
    "key": MOVIE_API_KEY,
    "movieNm": "Avengers"  # 검색할 영화 이름
}

# JSON 형식으로 요청
response = requests.get(f"{BASE_URL}.json", params=params)

# 응답 처리
if response.status_code == 200:
    data = response.json()  # JSON 응답 파싱
    movie_list = data.get("movieListResult", {}).get("movieList", [])
    for movie in movie_list:
        print(f"영화 제목: {movie.get('movieNm')}")
        print(f"개봉일: {movie.get('openDt')}")
        print(f"영화유형: {movie.get('typeNm')}")
        print(f"장르: {movie.get('genreAlt')}")
        print("-" * 20)
else:
    print(f"API 요청 실패: {response.status_code}")
