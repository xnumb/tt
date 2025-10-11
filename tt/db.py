import pymysql
from contextlib import contextmanager


class DB:
    """数据库操作类，支持上下文管理器和单例模式"""
    
    def __init__(self, db_name, pwd, host='127.0.0.1', port=3306, user='root'):
        self.db_name = db_name
        self.pwd = pwd
        self.host = host
        self.port = port
        self.user = user
        self.connect = None
        self.cursor = None
        self._is_connected = False

    def __enter__(self):
        """进入上下文管理器时自动连接"""
        self.conn()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文管理器时自动关闭连接"""
        self.close()
        return False

    def conn(self):
        """建立数据库连接"""
        if self._is_connected and self.connect:
            # 检查连接是否仍然有效
            try:
                self.connect.ping(reconnect=True)
                return
            except:
                pass
        
        self.connect = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.pwd,
            db=self.db_name,
            charset='utf8mb4'
        )
        self.cursor = self.connect.cursor(pymysql.cursors.DictCursor)
        self._is_connected = True

    def close(self):
        """关闭数据库连接"""
        if self.cursor:
            self.cursor.close()
        if self.connect:
            self.connect.close()
        self._is_connected = False

    def ensure_connected(self):
        """确保数据库已连接"""
        if not self._is_connected:
            self.conn()

    def query(self, sql, params=None):
        """查询数据"""
        self.ensure_connected()
        self.cursor.execute(sql, params or ())
        return self.cursor.fetchall()

    def query_one(self, sql, params=None):
        """查询单条数据"""
        self.ensure_connected()
        self.cursor.execute(sql, params or ())
        return self.cursor.fetchone()

    def insert(self, sql, params=None):
        """插入数据"""
        self.ensure_connected()
        self.cursor.execute(sql, params or ())
        self.connect.commit()
        return self.cursor.lastrowid

    def update(self, sql, params=None):
        """更新数据"""
        self.ensure_connected()
        self.cursor.execute(sql, params or ())
        self.connect.commit()
        return self.cursor.rowcount

    def delete(self, sql, params=None):
        """删除数据"""
        self.ensure_connected()
        self.cursor.execute(sql, params or ())
        self.connect.commit()
        return self.cursor.rowcount

    def execute(self, sql, params=None):
        """执行 SQL 语句"""
        self.ensure_connected()
        self.cursor.execute(sql, params or ())
        self.connect.commit()
        return self.cursor.rowcount

    def execute_many(self, sql, params_list):
        """批量执行 SQL 语句"""
        self.ensure_connected()
        self.cursor.executemany(sql, params_list)
        self.connect.commit()
        return self.cursor.rowcount

