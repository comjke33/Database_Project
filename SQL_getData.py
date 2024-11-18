import sqlite3

db_name = "project.db"
conn = sqlite3.connect(db_name)
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

#user_id로 감상한 영화 리스트 조회
def fetch_user_watched_movies(user_id):
    cursor.execute("""
    SELECT m.mID 
    FROM WatchedMovies wm
    JOIN Movie m ON wm.mID = m.mID
    WHERE wm.uID = ?;
    """, (user_id,))
    movies = cursor.fetchall()
    print(f"감상한 영화 {user_id}: {movies}")

#user_id로 위시 리스트 조회
def fetch_user_wishlist_movies(user_id):
    cursor.execute("""
    SELECT m.mID 
    FROM WishlistMovies wl
    JOIN Movie m ON wl.mID = m.mID
    WHERE wl.uID = ?;
    """, (user_id,))
    movies = cursor.fetchall()
    print(f"위시 리스트 {user_id}: {movies}")

#감상한 영화 추가
def add_watched_movie(uID, mID):
    try:
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

##### 커뮤니티 페이지 - DB 연동 #####
def get_db_connection():
    conn = sqlite3.connect
    conn.row_factory = sqlite3.Row
    return conn

def community_page():
    conn.row_factory = sqlite3.Row
    conn = get

#새로운 페이지 추가
def add_community_page(title, content, moviename, author):
    conn

if __name__ == "__main__":
    fetch_user_watched_movies("zxccyh")
    fetch_user_wishlist_movies("zxccyh")
    add_new_user("zxccyh", "1234", "남성", "26", "test@example.com")

conn.close()

