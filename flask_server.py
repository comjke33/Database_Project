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
        session['user_id'] = user_id  # 세션에 user_id 저장
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
    # community_data = SQL_getData.getCommunity()
    community_data = [{"author" : "Sally", "movie" : "Interstella", "title" : "Hi there", "content" : "Hi therethere"},
                       {"author" : "Sally", "movie" : "Interstella", "title" : "Hi there", "content" : "Hi therethere"},
                       {"author" : "Sally", "movie" : "Interstella", "title" : "Hi there", "content" : "Hi therethere"},
                       {"author" : "Sally", "movie" : "Interstella", "title" : "Hi there", "content" : "Hi therethere"},
                       {"author" : "Sally", "movie" : "Interstella", "title" : "Hi there", "content" : "Hi therethere"}
                       ]
    return render_template('community_page.html', community_data=community_data)

# 나의 개인정보 페이지
@app.route('/profile')
def profile_page():
    user_id = session.get('user_id') 
    user_email = session.get('user_email')
    
    user_data = [{"user_id": "comjke33", "user_gender":"여성", "user_age" : "21", "user_email":"comjke33@inu.ac.kr"}]
    # TODO
    # 내 영화 감상 리스트 가져오는 SQL
    user_watchedlist = [{"movieCd":"20148493", "movieNm":"어벤져스: 에이지 오브 울트론", "openDt":"20150423"}]

    # TODO
    # 내 영화 위시 리스트 가져오는 SQL
    user_wishlist = [{"movieCd":"20148493", "movieNm":"어벤져스: 에이지 오브 울트론", "openDt":"20150423"}]

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
def add_wishlist():
    movie = request.json  # Parse the JSON data from the request
    movie_name = movie.get('movieNm')
    movie_cd = movie.get('movieCd')
    movie_genre = movie.get('genreAlt')
    
    # TODO
    # 감상리스트에 추가하는 SQL 함수 호출

    return {'message': 'Movie added successfully'}, 200

@app.route('/delete-watched-movie', methods=['DELETE'])
def delete_watched_movie():
    movie = request.json
    movie_name = movie.get('movieNm')
    movie_cd = movie.get('movieCd')
    movie_genre = movie.get('genreAlt')

    # TODO
    # 감상리스트에서 삭제하는 SQL 함수 호출

    return {'message': 'Movie deleted successfully'}, 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
