import sqlite3
import requests
from config import MOVIE_API_KEY

db_name = "project.db"
conn = sqlite3.connect(db_name, check_same_thread=False)
cursor = conn.cursor()

##### 로그인 페이지 #####

#새로운 유저 추가(회원가입)
def signup(uID, password, gender, birthdate, email):
    try:
        #User 테이블
        cursor.execute("""
        INSERT INTO User (uID, Password, gender, birthdate, email)
        VALUES (?, ?, ?, ?, ?)
        """, (uID, password, gender, birthdate, email))
        
        #UserGenreScore 테이블
        cursor.execute("""
        INSERT INTO UserGenreScore (uID, drama, meloRomance, action, comedy, thriller, ero, horror, crime, animation, adventure, sf, fantasy, mystery, documentary, family, historical, war, performing, musical, western, other)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,(uID, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
        
        conn.commit()
        print(f"User '{uID}' 회원가입 완료")
    except sqlite3.IntegrityError as e:
        #중복 User 방지
        print(f"Error  '{uID}': {e}")

#로그인
def login(uID, password):
    try:
        #DB에서 ID로 password 가져오기
        cursor.execute("""
        SELECT Password 
        FROM User
        WHERE uID = ?""", (uID,))
        result = cursor.fetchone()

        if result:
            _password = result[0]
            if password == _password:
                print(f"로그인 성공")
                return True
            else:
                print(f"로그인 실패")
                return False
        else:
            print(f"존재하지 않는 사용자입니다.")
    except sqlite3.Error as e:
        print(f"오류 발생")

##### 내 프로필 #####

#user 정보 반환
def get_user_info(user_id):
    user_data = []
    try:
        cursor.execute("""
        SELECT uID, gender, birthdate, email
        FROM User
        WHERE uID = ?;
        """, (user_id,))
        row = cursor.fetchall()
            
        user_data.append({
            "user_id": row[0][0],     # uId
            "user_gender": row[0][1],      # gender
            "user_age": row[0][2],      # age
            "user_email": row[0][3]     # email
        })
    except sqlite3.Error as e:
        print(f"유저 데이터 읽기 오류: {e}")
    
    return user_data

#user_id로 감상한 영화 리스트 조회
def fetch_user_watched_movies(user_id):
    watched_list = []
    cursor.execute("""
    SELECT m.mID, m.mName, GROUP_CONCAT(mg.genre, ', ') AS Genres, wm.heart
    FROM WatchedMovies wm
    JOIN Movie m ON wm.mID = m.mID
    JOIN MovieGenre mg ON m.mID = mg.mID
    WHERE wm.uID = ?
    GROUP BY m.mID, m.mName;
    """, (user_id,))
    rows = cursor.fetchall()
    print(rows)
    for row in rows:
        watched_list.append({
            "movieCd": row[0],     # movieCd
            "movieNm": row[1],      # moviename
            "genreAlt": row[2],      # genre
            "heart": row[3]         #heart
        })
    print(watched_list)
    #print(f"감상한 영화 {user_id}: {rows[0][0]}")
    return watched_list

#user_id로 위시 리스트 조회
def fetch_user_wishlist_movies(user_id):
    wish_list = []
    
    cursor.execute("""
    SELECT m.mID, m.mName, GROUP_CONCAT(mg.genre, ', ') AS Genres
    FROM WishlistMovies wl
    JOIN Movie m ON wl.mID = m.mID
    JOIN MovieGenre mg ON m.mID = mg.mID
    WHERE wl.uID = ?
    GROUP BY m.mID, m.mName;
    """, (user_id,))
    rows = cursor.fetchall()

    for row in rows:
        wish_list.append({
        "movieCd": row[0],     # movieCd
        "movieNm": row[1],      # moviename
        "genreAlt": row[2],      # genre
    })
    #print(f"위시 리스트 {user_id}: {rows[0][0]}")
    return wish_list

#감상한 영화 추가
def add_watched_movie(uID, mID, movieNm):
    try:
        cursor.execute("SELECT 1 FROM Movie WHERE mID = ?",(mID,))
        movie_exists = cursor.fetchone()

        #영화가 없으면
        if not movie_exists:
            print(f"영화가 movie 테이블에 없음. 추가 중")
            add_movie_to_DB(movieNm, mID)
        
        # WatchedMovies 테이블에 새로운 영화 삽입
        cursor.execute("""
        INSERT INTO WatchedMovies (uID, mID)
        VALUES (?, ?)
        """, (uID, mID))
        conn.commit()
        print(f"감상한 영화 추가 {mID}  '{uID}'!")
    except sqlite3.IntegrityError as e:
        print(f"Error adding movie to watched list: {e}")
    except sqlite3.OperationalError as e:
        print(f"Operational error: {e}")

#감상하고 싶은 영화 추가
def add_wishlist_movie(uID, mID, movieNm):
    try:
        cursor.execute("SELECT 1 FROM Movie WHERE mID = ?",(mID,))
        movie_exists = cursor.fetchone()

        #영화가 없으면
        if not movie_exists:
            print(f"영화가 movie 테이블에 없음. 추가 중")
            add_movie_to_DB(movieNm, mID)

        # WishlistMovies 테이블에 새로운 영화 삽입
        cursor.execute("""
        INSERT INTO WishlistMovies (uID, mID)
        VALUES (?, ?)
        """, (uID, mID))
        conn.commit()
        print(f"위시리스트 추가 {mID}  '{uID}'!")
    except sqlite3.IntegrityError as e:
        print(f"Error adding movie to wishlist: {e}")
    except sqlite3.OperationalError as e:
        print(f"Operational error: {e}")

#감상한 영화 삭제
def delete_watched_movie(uID, mID):
    try:
        # WatchedMovies 테이블에서 삭제
        cursor.execute("""
        DELETE FROM WatchedMovies
        WHERE uID = ? AND mID = ?
        """, (uID, mID))

        #비어있지 않으면
        if cursor.rowcount > 0:
            conn.commit()
            print(f"감상한 영화 삭제 {mID}  '{uID}'!")
        else:
            print(f"No record found for user '{uID}' with movie ID {mID} in watched list.")
    except sqlite3.Error as e:
        print(f"Error deleting movie from watched list: {e}")

#감상하고 싶은 영화 삭제
def delete_wishlist_movie(uID, mID):
    try:
        # WishlistMovies 테이블에서 삭제
        cursor.execute("""
        DELETE FROM WishlistMovies
        WHERE uID = ? AND mID = ?
        """, (uID, mID))

        #비어있지 않으면
        if cursor.rowcount > 0:
            conn.commit()
            print(f"위시리스트 삭제 {mID}  '{uID}'!")
        else:
            print(f"No record found for user '{uID}' with movie ID {mID} in wishlist.")
    except sqlite3.Error as e:
        print(f"Error deleting movie from wishlist: {e}")

#감상한 영화 하트 +1
def press_heart_plus(uID, mID):
    try:
        cursor.execute("""
        SELECT genre
        FROM MovieGenre
        WHERE mID = ?
        """,(mID,))

        genres = cursor.fetchall()

        genre_parsing = {
            "드라마" : 'drama',
            "멜로/로맨스": 'meloRomance',
            "액션": 'action',
            "코미디": 'comedy',
            "스릴러": 'thriller',
            "성인물(에로)": 'ero',
            "공포(호러)": 'horror',
            "범죄": 'crime',
            "애니메이션": 'animation',
            "어드벤처": 'adventure',
            "SF": 'sf',
            "판타지": 'fantasy',
            "미스터리": 'mystery',
            "다큐멘터리": 'documentary',
            "가족": 'family',
            "사극": 'historical',
            "전쟁": 'war',
            "공연": 'performing',
            "뮤지컬": 'musical',
            "서부극": 'western',
            "기타": 'other'
        }

        for genre_row in genres:
            genre = genre_parsing[genre_row[0]]
            print({genre})
            query = f"""
            UPDATE UserGenreScore
            SET {genre} = {genre} + 1
            WHERE uID = ?;
            """
            cursor.execute(query, (uID,))
        conn.commit()

        cursor.execute("""
        UPDATE WatchedMovies
        SET heart = 1
        WHERE mID = ? AND uID = ?;
        """,(mID, uID))
        conn.commit()
        print(f"장르 점수 변경(증가) 완료")
    except sqlite3.OperationalError as e:
        print(f"SQL 에러 발생: {e}")
    except sqlite3.Error as e:
        print(f"데이터베이스 에러: {e}")

#감상한 영화 하트 -1
def press_heart_minus(uID, mID):
    try:
        cursor.execute("""
        SELECT genre
        FROM MovieGenre
        WHERE mID = ?
        """,(mID,))

        genres = cursor.fetchall()

        genre_parsing = {
            "드라마" : 'drama',
            "멜로/로맨스": 'meloRomance',
            "액션": 'action',
            "코미디": 'comedy',
            "스릴러": 'thriller',
            "성인물(에로)": 'ero',
            "공포": 'horror',
            "범죄": 'crime',
            "애니메이션": 'animation',
            "어드벤처": 'adventure',
            "SF": 'sf',
            "판타지": 'fantasy',
            "미스터리": 'mystery',
            "다큐멘터리": 'documentary',
            "가족": 'family',
            "사극": 'historical',
            "전쟁": 'war',
            "공연": 'performing',
            "뮤지컬": 'musical',
            "서부극": 'western',
            "기타": 'other'
        }

        for genre_row in genres:
            genre = genre_parsing[genre_row[0]]
            print({genre})
            query = f"""
            UPDATE UserGenreScore
            SET {genre} = {genre} - 1
            WHERE uID = ?;
            """
            cursor.execute(query, (uID,))
        conn.commit()
        cursor.execute("""
        UPDATE WatchedMovies
        SET heart = 0
        WHERE mID = ? and uID = ?;
        """,(mID,uID))
        conn.commit()

        print(f"장르 점수 변경(감소) 완료")
    except sqlite3.OperationalError as e:
        print(f"SQL 에러 발생: {e}")
    except sqlite3.Error as e:
        print(f"데이터베이스 에러: {e}")

##### 커뮤니티 페이지 - DB 연동 -> 공지페이지 #####

#현재 페이지 목록 출력
def getCommunity():
    community_data = []
    try:
        cursor.execute("""
        SELECT cID, title, content, mName, writer
        FROM COMMUNITY
        """)
        rows = cursor.fetchall()

        for row in rows:
            community_data.append({
                "cID": row[0],     
                "title": row[1],   
                "content": row[2], 
                "mName": row[3],
                "writer": row[4],    
            })
    except sqlite3.Error as e:
        print(f"커뮤니티 데이터 읽기 오류: {e}")
    
    return community_data

#새로운 페이지 추가
def add_new_post(title, content, mName, writer):
    try:
        cursor.execute("""
        INSERT INTO Community (title, content, mName, writer)
        VALUES (?, ?, ?, ?);
        """, (title, content, mName, writer))
        conn.commit()
        print(f"DB에 추가: '{title}' by {writer}")
    except sqlite3.Error as e:
        print(f"DB에 추가 실패: {e}")

# 페이지 삭제
def delete_post(cID):
    try:
        cursor.execute("""
        DELETE FROM Community
        WHERE cID = ?
        """, (cID,))
        conn.commit()  # 변경사항 저장
        print(f"게시글 ID {cID} 삭제 완료")
    except sqlite3.Error as e:
        print(f"게시글 삭제 실패: {e}")

##### DB에 영화 추가(API요청) #####
def add_movie_to_DB(movieNm, movieCd):
    # API 기본 URL 및 인증키
    BASE_URL = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList"

    # 요청 파라미터
    params = {
        "key": MOVIE_API_KEY,
        "movieNm": movieNm,  # 검색할 영화 이름
        "movieCd": "",
        "genreAlt": ""
    }

    # JSON 형식으로 요청
    response = requests.get(f"{BASE_URL}.json", params=params)

    # 응답 처리
    if response.status_code == 200:
        data = response.json()  # JSON 응답 파싱
        movie_list = data.get("movieListResult", {}).get("movieList", [])
        #DB에 저장
        for movie in movie_list:
            movie_cd = movie.get('movieCd')
            movieNm2 = movie.get('movieNm')
            genres = movie.get('genreAlt')

            if (movieNm == movieNm2) & (movie_cd == movieCd):
                cursor.execute("""
                INSERT OR IGNORE INTO Movie (mID, mName)
                VALUES (?, ?)
                """,(movie_cd, movieNm))

                if genres:
                    genre_list = [genre.strip() for genre in genres.split(",")]
                    for genre in genre_list:
                        cursor.execute("""
                        INSERT INTO MovieGenre (mID, genre)
                        VALUES (?, ?)
                        """,(movie_cd, genre))
        conn.commit()
        print(f"'{movieNm}' 영화와 장르가 추가됨")
    else:
        print(f"API 요청 실패: {response.status_code}")

##### 매칭 페이지 #####

# 가장 높은 점수를 가진 유저를 찾음
def get_matching_result(user_id):
    user_data = []
    try:
        cursor.execute("""
            WITH user_scores AS (
                SELECT *
                FROM UserGenreScore
                WHERE uID = ?
            ),
            score_difference AS (
                SELECT
                    u.uID AS other_uID,
                    (
                        COALESCE(ABS(u.drama - v.drama), 0) +
                        COALESCE(ABS(u.meloRomance - v.meloRomance), 0) +
                        COALESCE(ABS(u.action - v.action), 0) +
                        COALESCE(ABS(u.comedy - v.comedy), 0) +
                        COALESCE(ABS(u.thriller - v.thriller), 0) +
                        COALESCE(ABS(u.ero - v.ero), 0) +
                        COALESCE(ABS(u.horror - v.horror), 0) +
                        COALESCE(ABS(u.crime - v.crime), 0) +
                        COALESCE(ABS(u.animation - v.animation), 0) +
                        COALESCE(ABS(u.adventure - v.adventure), 0) +
                        COALESCE(ABS(u.sf - v.sf), 0) +
                        COALESCE(ABS(u.fantasy - v.fantasy), 0) +
                        COALESCE(ABS(u.mystery - v.mystery), 0) +
                        COALESCE(ABS(u.documentary - v.documentary), 0) +
                        COALESCE(ABS(u.family - v.family), 0) +
                        COALESCE(ABS(u.historical - v.historical), 0) +
                        COALESCE(ABS(u.war - v.war), 0) +
                        COALESCE(ABS(u.performing - v.performing), 0) +
                        COALESCE(ABS(u.musical - v.musical), 0) +
                        COALESCE(ABS(u.western - v.western), 0) +
                        COALESCE(ABS(u.other - v.other), 0)
                    ) AS total_difference
                FROM UserGenreScore u
                CROSS JOIN user_scores v
                WHERE u.uID != ?
            )
            SELECT 
                other_uID
            FROM score_difference
            ORDER BY total_difference ASC
        """, (user_id, user_id))
        
        rows = cursor.fetchall()  # Fetch all matching users
        
        # Add all matching users to user_data
        for row in rows:
            user_data.append({
                "user_id": row[0],  # uID of the matching user
            })
        
    except sqlite3.Error as e:
        print(f"유저 데이터 읽기 오류: {e}")
    
    return user_data



#if __name__ == "__main__":
    #fetch_user_watched_movies("zxccyh")
    #fetch_user_wishlist_movies("zxccyh")
    ###add_new_user("zxccyh", "1234", "남성", "26", "test@example.com")
    #get_user_info("zxccyh")
    #add_new_user("admin","admin","남성","26","test1@example.com")

#conn.close()