from collections import namedtuple
import doctest

from helper_scripts.utility import enum
from database.db_connection import DBConnection

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

db_connection = DBConnection.Instance().get_connection()


def question_from_topic(topic):
    cursor = db_connection.cursor()
    sql = 'SELECT * from questions_question where topic = %s limit 1'
    cursor.execute(sql, (topic))
    response = cursor.fetchone()
    cursor.close()
    return response


def question_from_sub_topic(sub_topic):
    cursor = db_connection.cursor()
    sql = 'SELECT * from questions_question where sub_topic = %s limit 1'
    cursor.execute(sql, (sub_topic))
    response = cursor.fetchone()
    cursor.close()
    return response


def video(question_id):
    cursor = db_connection.cursor()
    sql = 'SELECT video from questions_question where qid = %s'
    cursor.execute(sql, (question_id))
    return cursor.fetchone()['video']


def options_and_answer(question_id):
    cursor = db_connection.cursor()
    sql = 'SELECT o.option_text from questions_option o join ' \
        'questions_question q on o.qid_id = q.id where q.id = %s'
    cursor.execute(sql, (question_id))
    return answer(
        options=[item['option_text'] for item in cursor.fetchall()],
        correct=correct_answer(question_id))


def correct_answer(question_id):
    cursor = db_connection.cursor()
    sql = 'SELECT o.correct from questions_option o join questions_question q '\
        'on o.qid_id = q.id where q.id = %s'
    cursor.execute(sql, (question_id))
    answers = [item['correct'] for item in cursor.fetchall()]
    for index, answer in enumerate(answers):
        if answer == 1:
            return index


def subtopics():
    cursor = db_connection.cursor()
    sql = 'select distinct sub_topic from questions_question'
    cursor.execute(sql)
    response = cursor.fetchall()
    cursor.close()
    return response


if __name__ == "__main__":
    doctest.testmod()
