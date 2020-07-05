from itemadapter import ItemAdapter
import pymysql

db_info = {
    'host':'127.0.0.1',
    'port':'3306',
    'user':'root',
    'password':'root',
    'db':'pytest',
    'charset':'utf8mb4'
}

class ConnDB():
    def __init__(self):
        self.host = db_info['host']
        self.port = int(db_info['port'])
        self.user = db_info['user']
        self.password = db_info['password']
        self.db = db_info['db']
        self.charset = db_info['charset']
    
    def insertData(self, item):
        conn = pymysql.connect(host = self.host, port = self.port, 
                user = self.user, password = self.password, db = self.db)
        try:
            cur = conn.cursor()
            sqlStr = "INSERT INTO t_movie_info(movie_title, movie_datetime, movie_type_name) VALUES('%s', '%s', '%s') " %(item['movieTitle'], item['movieType'], item['movieDatetime'])
            cur.execute(sqlStr)
            cur.close()
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(e)
        finally:
            conn.close()
        
    

class MaoyanmoviePipeline:
    def process_item(self, item, spider):
        # 保存到数据库
        # print(DB_INFO)
        if item != '':
            obj = ConnDB()
            obj.insertData(item)
            return item
