from flask import Flask, render_template, redirect, request, session
from config import APP_KEY

app = Flask(__name__) 
app.secret_key = APP_KEY

# 기본 페이지가 login
@app.route('/')
def home():
    return redirect('/login')

# 로그인 화면
@app.route('/login', methods=['GET', 'POST'])
def login():
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
    user_id = session.get('user_id')  # 세션에서 user_id 가져오기
    if user_id:
        return render_template('home_page.html', user_id=user_id)
    return "No user_id found. Please log in.", 401

# 나의 개인정보 페이지
@app.route('/profile')
def profile_page():
    user_id = session.get('user_id') 
    user_email = session.get('user_email')
    
    # TODO
    # 내 영화 감상 리스트 가져오는 SQL

    # TODO
    # 내 영화 위시 리스트 가져오는 SQL

    
    if user_id and user_email:
        return render_template('profile_page.html', user_id=user_id)
    return "No user_id found. Please log in.", 401

# 개인정보 페이지
@app.route('/profile/<string:id>')
def profile_page():
    # TODO
    # 사용자의 id 및 이메일 저장
    user_id = ""
    user_email = ""
    
    # TODO
    # 사용자의 영화 감상 리스트 가져오는 SQL

    # TODO
    # 사용자의 영화 위시 리스트 가져오는 SQL

    
    if user_id and user_email:
        return render_template('profile_page.html', user_id=user_id)
    return "No user_id found. Please log in.", 401

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)
