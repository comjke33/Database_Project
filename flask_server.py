from flask import Flask, render_template, redirect, request, session
from config import APP_KEY

import API_BoxOffice, SQL_getData

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
    
    # TODO
    # 내 영화 감상 리스트 가져오는 SQL
    
    # TODO
    # 내 영화 위시 리스트 가져오는 SQL

    
    # if user_id and user_email:
    return render_template('profile_page.html', user_id=user_id)
    return "No user_id found. Please log in.", 401

# # 개인정보 페이지
# @app.route('/profile/<string:id>')
# def profile_page():
#     # TODO
#     # 사용자의 id 및 이메일 저장
#     user_id = ""
#     user_email = ""
    
#     # TODO
#     # 사용자의 영화 감상 리스트 가져오는 SQL

#     # TODO
#     # 사용자의 영화 위시 리스트 가져오는 SQL

    
#     if user_id and user_email:
#         return render_template('profile_page.html', user_id=user_id)
#     return "No user_id found. Please log in.", 401

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
