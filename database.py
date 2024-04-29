# DB connection config 파일에서 설정값 불러와 셋팅, 데이터베이스 연결.
import pymysql
import configparser

def __init__(self):
    config = configparser.ConfigParser()
    config.read('./dbconfig.ini')
    self.host = config['DEV']['HOST'] 
    self.database_name = config['DEV']['DATABASE_NAME'] 
    self.user = config['DEV']['USER'] 
    self.password = config['DEV']['PASSWORD']
    self.port = config['DEV']['PORT']
    self.charset = config['DEV']['CHARSET']        
    
        
def get_connection(self):
    self.conn = pymysql.connect(host=self.host,
                                user=self.user,
                                password=self.password,
                                db=self.database_name
                                )
    return self.conn

