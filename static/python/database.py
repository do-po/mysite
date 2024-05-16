# mysql 서버와의 연결부터 query문 질의까지
# class 생성

import pymysql

class MyDB:
    
    # 생성자 함수 생성

    def __init__(
            self, _host, _port, _user, _pass, _db
            ):
        
        # Class 내부에서 사용되는 독립 변수를 생성

        self.host = _host
        self.port = _port
        self.user = _user
        self.pw = _pass
        self.db = _db

    # Class 내장 함수 생성
        # DB server와 연결 -> 가상 공간 Cursor 생성 -> 
        # 매개변수 query문, data 값을 이용하여 -> 질의 보냄 (execute) ->
        # 결과 값을 받아오거나 DB 서버와 동기화 (fetchall or commit) -> DB 서버와 연결을 종료 (close)

    def db_execute(self, query, *data): # *data == data 매개변수의 갯수는 가변적이다

        # 데이터 베이스와 연결

        _db = pymysql.connect(
            host = self.host,
            port = self.port,
            user = self.user,
            password = self.pw,
            db = self.db
        )
        

        # 가상공간 Cursor 생성
            # pymysql의 커서들 중 DictCursor로 불러와야겠다 (값이 list 안의 dict 형태로 나옴)

        cursor = _db.cursor(pymysql.cursors.DictCursor)

        # 매개변수 query, data를 이용하여 질의 (질의가 DB에 바로 영향을 주는 구문 형태가 아니기에 cursor에서 구문을 실행하는 것)

        cursor.execute(query, data)

        # query가 select라면 결과값을 변수(result)에 저장
            # query가 길어지면 \n으로 줄을 나눠주기 때문에 좌, 우의 공백을 제거하는게 필요

        if query.strip().upper().startswith('SELECT'):
            result = cursor.fetchall()

        # query가 select가 아니라면 DB 서버와 동기화 하고 변수(result)는 Query Done 문자를 대입

        else:
            _db.commit()
            result = 'Query Done'

        # DB 서버와의 연결을 종료

        _db.close()

        # 결과(result) return

        return result