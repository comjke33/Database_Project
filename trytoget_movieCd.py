import requests
import sqlite3
from config import MOVIE_API_KEY

####API를 이용하여 DB에 넣을 movieCD를 받아오는 코드

# API 기본 URL 및 인증키
BASE_URL = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList"


conn = sqlite3.connect("project.db")
cursor = conn.cursor()
mn = "어벤져스"
# 요청 파라미터 설정
params = {
    "key": MOVIE_API_KEY,
    "movieNm": mn,
    "movieCd": "",
    "genreAlt": ""        
}

# JSON 형식으로 요청
response = requests.get(f"{BASE_URL}.json", params=params)

# 응답 데이터 확인
if response.status_code == 200:
    data = response.json()
    movie_list = data.get("movieListResult", {}).get("movieList", [])
    for movie in movie_list:
        movie_cd = movie.get('movieCd')
        movieNm = movie.get('movieNm')
        genre = movie.get('genreAlt')

        #중복방지
        #cursor.execute("SELECT COUNT(*) FROM Movie WHERE mID = ?", (movie_cd,))         
        
        #cursor.execute("""INSERT INTO Movie (mID) VALUES (?)""", (movie_cd,))
        if(movieNm == mn):
            print(movie.get('movieNm'))
            print(movie.get('movieCd'))
            print(genre)
else:
    print(f"movidCd 추출 실패: {response.status_code}")

conn.close()