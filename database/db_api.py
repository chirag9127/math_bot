from collections import namedtuple
import doctest
import random

from helper_scripts.utility import enum
from database.db_connection import DBConnection
from messenger_bot.logger import log

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


def question_from_topic(topic):
    sql = 'SELECT question_text, id from questions_question where ' \
        'topic = "{}" ' \
        'and deleted = 0 and correct = TRUE order by rand() limit 1'.format(
            topic)
    cursor = execute_sql(sql)
    response = cursor.fetchone()
    cursor.close()
    return response


def question_from_sub_topic(sub_topic):
    sql = 'SELECT * from questions_question where sub_topic = "{}" and ' \
        'correct = TRUE limit 1'.format(sub_topic)
    cursor = execute_sql(sql)
    response = cursor.fetchone()
    cursor.close()
    return response


def has_video(question_id):
    sql = 'select video_added from questions_question where id = {}'.format(
        question_id)
    cursor = execute_sql(sql)
    val = cursor.fetchone()['video_added']
    cursor.close()
    if val == 1:
        return True
    return False


def video(question_id):
    sql = 'SELECT video from questions_question where id = {}'.format(
        question_id)
    cursor = execute_sql(sql)
    video = cursor.fetchone()['video']
    cursor.close()
    return video


def options_and_answer(question_id):
    sql = 'SELECT o.id, o.option_text, o.correct from questions_option ' \
        'o join questions_question q on o.qid_id = q.id ' \
        'where q.id = {}'.format(question_id)
    cursor = execute_sql(sql)
    options = cursor.fetchall()
    cursor.close()
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
    sql = 'select distinct sub_topic from questions_question'
    cursor = execute_sql(sql)
    response = cursor.fetchall()
    cursor.close()
    return response


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


if __name__ == "__main__":
    doctest.testmod()
