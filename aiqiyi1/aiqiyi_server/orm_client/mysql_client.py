import pymysql

class MysqlClient:
    #单例模式
    __instance = None
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)

        return cls.__instance

    def __init__(self):
        self.client = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='123zgh',
            database='test1',
            charset='utf8',
            autocommit=True
        )
        self.cursor = self.client.cursor(
            pymysql.cursors.DictCursor
        )

    def my_select(self,sql,value=None):
        self.cursor.execute(sql,value)
        res = self.cursor.fetchall()
        return res

    def my_execute(self,sql,values):
        try:
            self.cursor.execute(sql,values)

        except Exception as e:
            print(e)

    def close(self):
        self.cursor.close()
        self.client.close()