from collections import namedtuple
import doctest
import random

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
    sql = 'SELECT question_text, id from questions_question where topic = %s and deleted = 0 '\
        'and correct = TRUE order by rand() limit 1'
    cursor.execute(sql, (topic))
    response = cursor.fetchone()
    cursor.close()
    return response


def question_from_sub_topic(sub_topic):
    cursor = db_connection.cursor()
    sql = 'SELECT * from questions_question where sub_topic = %s and correct = TRUE limit 1'
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
    sql = 'SELECT o.id, o.option_text, o.correct from questions_option ' \
        'o join questions_question q on o.qid_id = q.id where q.id = %s'
    cursor.execute(sql, (question_id))
    options = cursor.fetchall()
    while len(options) > 3:
        item = random.choice(options)
        if item['correct'] == 1:
            continue
        options.remove(item)
    return answer(
        options=[{'id': opt['id'], 'text': opt['option_text']}
                 for opt in options],
        correct=correct_answer(options))


def correct_answer(options):
    for opt in options:
        if opt['correct'] == 1:
            return opt['id']


def subtopics():
    cursor = db_connection.cursor()
    sql = 'select distinct sub_topic from questions_question'
    cursor.execute(sql)
    response = cursor.fetchall()
    cursor.close()
    return response


if __name__ == "__main__":
    doctest.testmod()
