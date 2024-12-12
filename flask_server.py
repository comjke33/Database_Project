from flask import Flask, render_template, redirect, request, session
from config import APP_KEY

import API_BoxOffice, SQL_getData, API_MovieInfo

app = Flask(__name__) 
app.secret_key = APP_KEY

# 기본 페이지가 login
@app.route('/')
def home():
    return redirect('/login')

# 로그인 화면
@app.route('/login', methods=['GET', 'POST'])
def login():
    session["dailyBoxOffice_movie"] = API_BoxOffice.getDailyBoxOffice()
    session["weeklyBoxOffice_movie"] = API_BoxOffice.getWeeklyBoxOffice()

    if request.method == 'POST':
        
        user_id = request.form.get('user_id')
        password = request.form.get('password')
        

        #user_id = 'admin'
        #password = 'admin'

        session['user_id'] = user_id  # 세션에 user_id 저장
        if (SQL_getData.login(user_id, password)):
            return redirect('/home')
    return render_template('login_page.html')

# TODO
# 로그인 실패했을 때 

# 기본 페이지
@app.route('/home')
def home_page():
    dailyBoxOffice_movie = session["dailyBoxOffice_movie"]
    weeklyBoxOffice_movie = session["weeklyBoxOffice_movie"]

    #return render_template('test.html')
    if dailyBoxOffice_movie and weeklyBoxOffice_movie:
        return render_template('home_page.html', dailyBoxOffice_movie=dailyBoxOffice_movie, weeklyBoxOffice_movie=weeklyBoxOffice_movie)
    return "No user_id found. Please log in.", 401

# 커뮤니티 페이지
@app.route('/community')
def community_page():
    community_data = SQL_getData.getCommunity()
    """
    community_data = [{"author" : "Sally", "movie" : "Interstella", "title" : "Hi there", "content" : "Hi therethere"},
                       {"author" : "Sally", "movie" : "Interstella", "title" : "Hi there", "content" : "Hi therethere"},
                       {"author" : "Sally", "movie" : "Interstella", "title" : "Hi there", "content" : "Hi therethere"},
                       {"author" : "Sally", "movie" : "Interstella", "title" : "Hi there", "content" : "Hi therethere"},
                       {"author" : "Sally", "movie" : "Interstella", "title" : "Hi there", "content" : "Hi therethere"}
                       ]
                       """
    return render_template('community_page.html', community_data=community_data)

# 나의 개인정보 페이지
@app.route('/profile')
def profile_page():
    user_id = session.get('user_id') 
    user_email = session.get('user_email')
    
    user_data = SQL_getData.get_user_info(user_id)
    # TODO
    # 내 영화 감상 리스트 가져오는 SQL
    user_watchedlist = SQL_getData.fetch_user_watched_movies(user_id)
    #user_watchedlist = [{"movieCd":"20148493", "movieNm":"어벤져스: 에이지 오브 울트론", "genre":"스릴러"}]

    # TODO
    # 내 영화 위시 리스트 가져오는 SQL
    user_wishlist = SQL_getData.fetch_user_wishlist_movies(user_id)
    #user_wishlist = [{"movieCd":"20148493", "movieNm":"어벤져스: 에이지 오브 울트론", "openDt":"20150423"}]
    
    # if user_id and user_email:
    return render_template('profile_page.html', user_data=user_data, user_watchedlist=user_watchedlist, user_wishlist=user_wishlist)
    return "No user_id found. Please log in.", 401 

# 영화 검색 API 엔드포인트
@app.route('/search', methods=['GET'])
def search_movie():
    query = request.args.get('query')
    data = API_MovieInfo.getMovieInfo(query)
    return data

@app.route('/add-watchedlist', methods=['POST'])
def add_watchedlist():
    movie = request.json  # Parse the JSON data from the request
    movie_name = movie.get('movieNm')
    movie_cd = movie.get('movieCd')
    movie_genre = movie.get('genreAlt')
    user_id = session.get('user_id')
    # TODO
    # 감상리스트에 추가하는 SQL 함수 호출
    SQL_getData.add_watched_movie(user_id, movie_cd, movie_name)
    return {'message': 'Movie added successfully'}, 200

@app.route('/delete-watched-movie', methods=['DELETE'])
def delete_watchedlist():
    movie = request.json
    movie_name = movie.get('movieNm')
    movie_cd = movie.get('movieCd')
    movie_genre = movie.get('genreAlt')
    
    # TODO
    # 감상리스트에서 삭제하는 SQL 함수 호출
    user_id = session.get('user_id')
    SQL_getData.delete_watched_movie(user_id, movie_cd)
    return {'message': 'Movie deleted successfully'}, 200

@app.route('/heart-watched-movie', methods=['PATCH'])
def heart_watched_movie():
    user_id = session.get('user_id')
    data = request.json
    movie_cd = data.get('movieCd')  # Unique movie code
    hearted = data.get('hearted')  # New hearted status (True or False)

    # TODO
    # heart 업데이트 SQL 호출
    if (hearted):
        SQL_getData.press_heart_plus(user_id, movie_cd)
    else:
        SQL_getData.press_heart_minus(user_id, movie_cd)

    #SQL_getData.update_heart(user_id, movie_cd, hearted)
    return {'message': 'Movie deleted successfully'}, 200  

@app.route('/add-wishlist', methods=['POST'])
def add_wishlist():
    movie = request.json  # Parse the JSON data from the request
    movie_name = movie.get('movieNm')
    movie_cd = movie.get('movieCd')
    movie_genre = movie.get('genreAlt')
    user_id = session.get('user_id')
    # TODO
    # 위시리스트에 추가하는 SQL 함수 호출
    SQL_getData.add_wishlist_movie(user_id, movie_cd, movie_name)
    return {'message': 'Movie added successfully'}, 200

@app.route('/delete-wish-movie', methods=['DELETE'])
def delete_wishlist():
    movie = request.json
    movie_name = movie.get('movieNm')
    movie_cd = movie.get('movieCd')
    movie_genre = movie.get('genreAlt')

    # TODO
    # 위시리스트에서 삭제하는 SQL 함수 호출
    user_id = session.get('user_id')
    SQL_getData.delete_wishlist_movie(user_id, movie_cd)
    return {'message': 'Movie deleted successfully'}, 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
