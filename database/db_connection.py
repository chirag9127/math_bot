import pymysql
import pymysql.cursors

from database.config import get_params
from helper_scripts.singleton import Singleton


@Singleton
class DBConnection(object):

    def __init__(self):
        self.params = get_params()
        self.conn = pymysql.connect(
            host=self.params.host,
            user=self.params.username, password=self.params.password,
            db='ceredron', charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)

    def get_connection(self):
        return self.conn

    def __del__(self):
        self.conn.close()
