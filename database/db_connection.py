import pymysql
import pymysql.cursors

from database.config import get_params
from helper_scripts.singleton import Singleton
from messenger_bot.logger import log


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


def execute_sql(query):
    db_connection = DBConnection.Instance().get_connection()
    try:
        cursor = db_connection.cursor()
        cursor.execute(query)
    except:
        db_connection.close()
        cursor = db_connection.cursor()
        cursor.execute(query)
        log("error! execute sql {}".format(query))
    return cursor
