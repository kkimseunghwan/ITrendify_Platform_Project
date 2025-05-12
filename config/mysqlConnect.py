import pymysql

# 동작 관련 클래스로 객체화 하여 사용하는 것이 좋을 것 같음.
# 예시)
# mysql_con = mysqlCon()
# mysql_con.connect_to_mysql()
# mysql_con.close_connection()

# 데이터베이스 연결 클래스
class mysqlConnection:
    def __init__(self):
        pass

    # 데이터베이스 연결
    #   in window : ssh -L 8080:localhost hwan@192.168.0.56
    @staticmethod
    def connect_to_mysql():
        try:
            # pymysql은 DictCursor도 지원함 (원한다면)
            conn = pymysql.connect(
                host="localhost",       # MySQL 서버 주소
                port=8080,              # 열려있는 포트 번호
                user="Hwan",            # MySQL 사용자 이름
                password="34933493",    # MySQL 비밀번호
                database="TESTDB",      # 사용할 데이터베이스 이름
                charset="utf8mb4",      # 문자 인코딩
                autocommit=True        # 명시적으로 commit할 수 있도록 설정
            )
            cursor = conn.cursor()
            return conn, cursor

        except pymysql.MySQLError as e:
            print(f"MySQL 연결 오류: {e}")
            return None, None


    # 연결 종료
    @staticmethod
    def close_connection(conn, cursor):
        cursor.close()
        conn.close()
        print("MySQL 연결 종료")    
            

# 사용 테스트
if __name__ == "__main__":
    # 데이터베이스 연결
    conn, cursor = mysqlConnection.connect_to_mysql()


    if conn is None or cursor is None:
        print("DB 연결 실패. 프로그램을 종료합니다.")
    else:
        try:
            # 데이터베이스 버전 확인
            cursor.execute("SELECT VERSION();")
            version = cursor.fetchone()
            print("MySQL Version:", version)

            # 테이블 목록 조회  
            cursor.execute("SHOW TABLES")
            rows = cursor.fetchall()
            for row in rows:
                print(row)

            # 테이블 데이터 조회
            cursor.execute("SELECT * FROM job_posting")
            rows = cursor.fetchall()
            for row in rows:
                print(row)

        except Exception as e:
            print(f"쿼리 실행 중 오류 발생: {e}")
        finally:
            # 연결 종료
            mysqlConnection.close_connection(conn, cursor)


    