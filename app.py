# flask 프레임 워크 안의 특정 기능들을 로드
# flask, html을 text로 받아오는 render_template, request, 페이지 이동하는 redirect
    # url_for는 외부 데이터 경로 지정하는 것

from flask import Flask, render_template, request, redirect, url_for, session

# mysql과 연동을 하는 라이브러리 로드

import pymysql
from datetime import timedelta

# 쿼리문들이 모여있는 queries 로드

from static.python import queries

# 환경 변수 dotenv 로드

from dotenv import load_dotenv
import os

# .env 파일을 로드

load_dotenv()

# database에 연결하는 MyDB Class 로드

from static.python.database import MyDB

# Flask라는 class 생성 (인자를 파일명으로 받아옴, 파일명이 이 파일의 이름일 경우 __name__)

app = Flask(__name__)

# secret_key 설정 (session data 암호화 키)

app.secret_key = os.getenv('secret_key')

# 세션 데이터의 생명주기(지속시간)을 설정

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds= 15)

# MyDB Class 생성

mydb = MyDB(
    os.getenv('host'),
    os.getenv(int('port')),
    os.getenv('user'),
    os.getenv('password'),
    os.getenv('db_name'),
)

# 메인페이지 api 생성
    # 로그인 화면

@app.route("/")
def sign_in():
    
    # 세션에 데이터가 존재한다면 ?
        # /index로 다시 보내서 main으로 보내기 (로그인을 이미 했다면 다시 로그인 화면을 띄워주지 않는 것)

    if 'user_id' in session:
        return redirect('/index')
    
    # 세션에 데이터가 없다면 ?
        # 로그인이 되어있지 않는다면 로그인 화면 보여주는 것

    else:

        # 주소로 접속 요청이 들어왔을 때 state라는 데이터가 존재하면

        try: # 로그인이 실패해서 redirect로 state가 2 인 값을 받아오는 경우
            _state = request.args['state']

        # 예외가 발생

        except: # 처음 로그인을 하는 경우
            _state = "1"

        # log_in.html과 state를 되돌려준다.
        
        return render_template('log_in.html', state = _state)

# 로그인 화면에서 id, password 데이터를 보내는 api 생성

@app.route("/main", methods=['post'])
def main():
    # 유저가 보낸 데이터 == id, pw 2개
    # 유저가 보낸 id 값의 key -> input_id로 잡아보자
    # 유저가 보낸 pw 값의 key -> input_pass로 잡아보자

    _id = request.form['input_id']
    _pass = request.form['input_pass']

    # 받아온 데이터를 확인 (어디서 나온 정보인 지 확인하기 위해 주소 식별자도 넣어주면 쉬움)

    print(f'/main[post] -> 유저 id : {_id}, pw : {_pass}')

    # 유저가 보낸 데이터를 DB server의 table data와 비교

    # 함수를 호출

    db_result = mydb.db_execute(queries.log_in_query, _id, _pass)

    # 로그인의 성공 여부 == db_result가 존재 여부

    # 로그인 성공 경우
        # main.html return

    if db_result:

        # 로그인이 성공하는 경우  session에 데이터를 저장
            # session 역시 dict 형태이기에 dict에 새 key:value 저장하는 형식으로 생성

        session['user_id']  = _id
        session['user_pass'] = _pass

        return redirect('/index')
        # frontend 아직 안 만들었는데 테스트 하고 싶은 경우(postman 같은거)
        # 위의 return 주석 처리 하고 아래 결과 나오는 지 확인하면 됨
        # return 'Login OK'

    # 로그인 실패 경우
        # login 화면인 '/' 으로 되돌아가면서 state 변수의 값을 1이 아닌 수로 설정 후 보내준다.

    else:
        return redirect('/?state=2')
        # return 'Login Fail'

# index 주소 api 생성

@app.route('/index')
def index2():
    
    # 세션에 데이터가 존재한다면 main.html 되돌려준다
    if 'user_id' in session:
        return render_template('/main.html')

    # 세션에 데이터가 존재하지 않는다면 login 화면 되돌려준다
    else:
        return redirect('/')

# 회원 가입 화면을 보여주는 api 생성

@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')

# id 존재 유무를 판단하는 api

@app.route('/check_id', methods = ['post'])
def check_id():
    # front-end에서 비동기 통신(ajax)으로 보내는 id 값을 변수에 저장
    _id = request.form['input_id']
    
    # 유저에게 받은 데이터 확인 (로그)

    print(f"/check_id[post] -> 유저 id : {_id}")

    # 유저가 보낸 id 값이 사용 가능한가?
        # 조건문 == 해당하는 id로 table에 데이터가 존재하는가 ?

    db_result = mydb.db_execute(queries.check_id_query, _id)

    # id가 사용 가능한 경우 == db_result 값이 없을 때

    if db_result:
        result = "0"

    else:
        result = "1"

    return result

# 회원 정보를 받아서 DB에 삽입을 하는 api

@app.route('/sign_up2', methods = ['post'])
def sign_up2():
    # 유저가 보낸 데이터를 변수에 저장


    _id = request.form['input_id']
    _pass = request.form['input_pass']
    _name = request.form['input_name']

    # 유저가 보낸 데이터 확인 (로그)

    print(f'/sign_up2[post] 유저 id : {_id}, password : {_pass}, 이름 : {_name}')

    # 함수 호출 [에러가 발생하는 경우가 있으니 (ID 삽입할 때 다른 사람이랑 하필 겹쳐서 안 들어가지거나 서버 오류거나 등등) try 생성]

    try:
        db_result = mydb.db_execute(queries.sign_up_query, _id, _pass, _name)
        print(db_result) # 이거 사실 필요 없긴한데 (어차피 Query Done 나오니까) 잘 들어갔는 지 내용 확인하려고 넣는 구문

    except:
        db_result = "3" # 왜 log_in으로 가려고 하지 ?? sign_up으로 가는게 더 좋지 않을까 싶은데 음... 그래야 다시 id 넣어서 회원가입 시도할텐데 말야. log_in으로 가면 다시 sign_up으로 가는 버튼 눌러야 되잖아

    # 로그인 화면으로 되돌아간다

    if db_result == "3":
        return redirect(f'/?state={db_result}')
    else:
        return redirect('/')
    
# 로그아웃
@app.route('/log_out')
def log_out():
    
    # 세션 데이터를 제거

    # session.pop('user_id', None)
    # session.pop('user_pass', None)
    session.clear()

    # 로그인 페이지로 이동

    return redirect('/')














# 웹 서버를 실행
    # flask run 돌릴거라 아래는 cmd 점검용

# app.run(debug= True)
