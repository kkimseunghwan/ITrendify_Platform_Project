from config.mysqlConnect import mysqlConnection
from OriginData import OriginData
import pymysql

# 지금 DB가 2개 계획 중.
# 1. 원본 데이터
# 2. 다대다 연결 중심 데이터

# 추후 전처리 후 저장되는 테이블도 계획중.
class OriginDataDAO:
    def __init__(self):
        pass

    def insertDataAll(self):
        pass

    def insertOriginData(self, originData: OriginData):
        try:
            conn, cursor = mysqlConnection.connect_to_mysql()

            sql = """
                INSERT INTO job_posting (title, company, location, description, created_at)
                VALUES (%s, %s, %s, %s, %s)
            """

            values = (
                originData.title,
                originData.company,
                originData.location,
                originData.description,
                originData.created_at
            )
            
            cursor.execute(sql, values)
            conn.commit()

        except pymysql.MySQLError as e:
            print(f"DB 삽입 오류: {e}")
            if conn:
                conn.rollback()
        finally:
            mysqlConnection.close_connection(conn, cursor)

    