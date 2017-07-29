from config import get_params
from helper_scripts.utility import enum
import pymysql.cursors


topic = enum(
    ARITHMETIC='Arithmetic',
    ALGEBRA='Algebra',
    STATS='Statistics',
    FACTORS='Factors and Multiples',
    GEOMETRY='Geometry',
    AGREEMENT='Agreement',
    WORD_PROBLEMS='Word Problems',
    TRIANGLES='Triangles',
    WORD_PROBLEM='Word Problem',
    COORDINATE_GEO='Coordinate Geometry'
    )


def get_connection():
    params = get_params()
    connection = pymysql.connect(
        host=params.host, user=params.username,
        password=params.password, db='ceredron',
        charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    return connection


def video(conn, question):
    pass


def answer_options(conn, question):
    pass


def right_answer(conn, question):
    pass

