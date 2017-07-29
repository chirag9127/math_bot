from config import get_params
from helper_scripts.utility import enum
from collections import namedtuple
import pymysql.cursors
import doctest

answer = namedtuple('answer', 'options, correct')

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
    cursor = conn.cursor()
    sql = 'SELECT video from questions_question where question_text = %s'
    cursor.execute(sql, (question))
    return cursor.fetchone()['video']


def options_and_answer(conn, question):
    cursor = conn.cursor()
    sql = 'SELECT o.option_text from questions_option o join questions_question q on o.qid_id = q.id where q.question_text = %s'
    cursor.execute(sql, (question))
    return answer(
        options=[item['option_text'] for item in cursor.fetchall()],
        correct=correct_answer(conn, question))


def correct_answer(conn, question):
    cursor = conn.cursor()
    sql = 'SELECT o.correct from questions_option o join questions_question q on o.qid_id = q.id where q.question_text = %s'
    cursor.execute(sql, (question))
    answers = [item['correct'] for item in cursor.fetchall()]
    for index, answer in enumerate(answers):
        if answer == 1:
            return index


if __name__ == "__main__":
    doctest.testmod()
