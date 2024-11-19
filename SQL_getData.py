import sqlite3

db_name = "project.db"
conn = sqlite3.connect(db_name, check_same_thread=False)
cursor = conn.cursor()

##### 로그인 페이지 #####

#새로운 유저 추가(회원가입)
def add_new_user(uID, password, gender, age, email):
    try:
        cursor.execute("""
        INSERT INTO User (uID, Password, gender, age, email)
        VALUES (?, ?, ?, ?, ?)
        """, (uID, password, gender, age, email))
        conn.commit()
        print(f"User '{uID}' 추가")
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
        SELECT uID, gender, age, email
        FROM User
        WHERE uID = ?;
        """, (user_id,))
        row = cursor.fetchall()
        row = row[0]
        user_data.append({
            "user_id": row[0],     # uId
            "user_gender": row[1],      # gender
            "user_age": row[2],      # age
            "user_email": row[3]     # email
        })
    except sqlite3.Error as e:
        print(f"유저 데이터 읽기 오류: {e}")
    
    return user_data

#user_id로 감상한 영화 리스트 조회
def fetch_user_watched_movies(user_id):
    watched_list = []
    cursor.execute("""
    SELECT m.mID, mName, Genre
    FROM WatchedMovies wm
    JOIN Movie m ON wm.mID = m.mID
    WHERE wm.uID = ?;
    """, (user_id,))
    rows = cursor.fetchall()

    for row in rows:
        watched_list.append({
            "movieCd": row[0],     # writer
            "movieNm": row[1],      # moviename
            "Genre": row[2],      # title
            "content": row[3]     # content
        })

    print(f"감상한 영화 {user_id}: {rows[0][0]}")
    return watched_list

#user_id로 위시 리스트 조회
def fetch_user_wishlist_movies(user_id):
    wish_list = []
    cursor.execute("""
    SELECT m.mID 
    FROM WishlistMovies wl
    JOIN Movie m ON wl.mID = m.mID
    WHERE wl.uID = ?;
    """, (user_id,))
    rows = cursor.fetchall()

    for row in rows:
        wish_list.append({
        "movieCd": row[0],     # writer
        "movieNm": row[1],      # moviename
        "Genre": row[2],      # title
        "content": row[3]     # content
    })
    print(f"위시 리스트 {user_id}: {rows[0][0]}")
    return wish_list

#감상한 영화 추가
def add_watched_movie(uID, mID):
    try:
        cursor.execute("SELECT 1 FROM Movie WHERE mID = ?",(mID,))
        movie_exists = cursor.fetchone()

        #영화가 없으면
        if not movie_exists:
            print(f"영화가 movie 테이블에 없음. 추가 중")
            #add_to_movie(mID)
        
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
def add_wishlist_movie(uID, mID):
    try:
        cursor.execute("SELECT 1 FROM Movie WHERE mID = ?",(mID,))
        movie_exists = cursor.fetchone()

        #영화가 없으면
        if not movie_exists:
            print(f"영화가 movie 테이블에 없음. 추가 중")
            #add_to_movie(mID)

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
def press_heart(uID, mID):
    genres = []
    try:
        cursor.execute("""
        SELECT genre
        FROM Movie
        WHERE mID = ?
        """,(mID))
    
        rows = cursor.fetchall()
        genres = [row[0] for row in rows]
        for genre in genres:
            query = f"""
            UPDATE UserGenreScore
            SET {genre} = {genre} + 1
            WHERE uID = ?;
            """
            cursor.execute(query, (uID))
        conn.commit()
        print(f"장르 점수 변경(증가) 완료")
    except sqlite3.OperationalError as e:
        print(f"SQL 에러 발생: {e}")
    except sqlite3.Error as e:
        print(f"데이터베이스 에러: {e}")

#감상한 영화 하트 -1
def press_heart(uID, mID):
    genres = []
    try:
        cursor.execute("""
        SELECT genre
        FROM Movie
        WHERE mID = ?
        """,(mID))
    
        rows = cursor.fetchall()
        genres = [row[0] for row in rows]
        for genre in genres:
            query = f"""
            UPDATE UserGenreScore
            SET {genre} = {genre} - 1
            WHERE uID = ?;
            """
            cursor.execute(query, (uID))
        conn.commit()
        print(f"장르 점수 변경(감소) 완료")
    except sqlite3.OperationalError as e:
        print(f"SQL 에러 발생: {e}")
    except sqlite3.Error as e:
        print(f"데이터베이스 에러: {e}")


##### 커뮤니티 페이지 - DB 연동 -> 공지페이지 #####

#현재 페이지 목록 출력
def community_page():
    community_data = []
    try:
        cursor.execute("""
        SELECT writer, moviename, title, content
        FROM COMMUNITY
        """)
        rows = cursor.fetchall()

        for row in rows:
            community_data.append({
                "author": row[0],     # writer
                "movie": row[1],      # moviename
                "title": row[2],      # title
                "content": row[3]     # content
            })
    except sqlite3.Error as e:
        print(f"커뮤니티 데이터 읽기 오류: {e}")
    
    return community_data

#새로운 페이지 추가
def add_new_post(title, content, moviename, writer):
    try:
        cursor.execute("""
        INSERT INTO COMMUNITY (title, content, moviename, writer)
        VALUES (?, ?, ?, ?)
        """, (title, content, moviename, writer))
        conn.commit()
        print(f"DB에 추가: '{title}' by {writer}")
    except sqlite3.Error as e:
        print(f"DB에 추가 실패: {e}")

# 페이지 삭제
def delete_post(cID):
    try:
        cursor.execute("""
        DELETE FROM COMMUNITY
        WHERE cID = ?
        """, (cID,))
        conn.commit()  # 변경사항 저장
        print(f"게시글 ID {cID} 삭제 완료")
    except sqlite3.Error as e:
        print(f"게시글 삭제 실패: {e}")

##### DB에 영화 추가(API요청) #####
def add_movie_to_DB():
    return 0

#if __name__ == "__main__":
    #fetch_user_watched_movies("zxccyh")
    #fetch_user_wishlist_movies("zxccyh")
    ###add_new_user("zxccyh", "1234", "남성", "26", "test@example.com")
    #get_user_info("zxccyh")
    #add_new_user("admin","admin","남성","26","test1@example.com")

#conn.close()