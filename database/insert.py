from database.db_connection import DBConnection
from collections import namedtuple
import ast

db_connection = DBConnection.Instance().get_connection()

user_request = namedtuple('user_request', 'id, query')

user_response = namedtuple('user_response', 'intent, entities, response, sender_id')

user_answer = namedtuple('user_answer', 'sender_id, question_id, answer, is_correct')


def insert_user_request(request_id, request):
    with db_connection.cursor() as cursor:
        sql = 'INSERT INTO user_request (id, sender_id, query) VALUES (%s, %s, %s)'
        values = parse_request_data(request)
        if values:
            cursor.execute(sql, (request_id, values.id, values.query))
            db_connection.commit()


def parse_request_data(request):
    data = ast.literal_eval(request)
    if 'message' in data['entry'][0]['messaging'][0].keys():
        return user_request(
            id=data['entry'][0]['messaging'][0]['sender']['id'],
            query=data['entry'][0]['messaging'][0]['message']['text']
            )


def insert_user_response(response_id, response):
    with db_connection.cursor() as cursor:
        sql_to_request = 'UPDATE user_request SET intent = %s, entities = %s WHERE id=%s'
        values = parse_response_data(response)
        cursor.execute(sql_to_request, (values.intent, values.entities, response_id))
        sql_to_response = 'INSERT INTO user_response (id, sender_id, response) VALUES (%s, %s, %s)'
        cursor.execute(sql_to_response, (response_id, values.sender_id, values.response))
    db_connection.commit()


def parse_response_data(response):
    data = ast.literal_eval(response)
    return user_response(
        intent=data['result']['metadata']['intentName'],
        entities=str(data['result']['parameters']),
        response=data['result']['fulfillment']['speech'],
        sender_id=data['sessionId']
    )


def insert_user_question(response_id, sender_id, question):
    with db_connection.cursor() as cursor:
        sql = 'INSERT INTO questions_given (id, sender_id, question_id) VALUES (%s, %s, %s)'
        question_id = parse_question(question)
        cursor.execute(sql, (response_id, sender_id, question_id))
    db_connection.commit()


def parse_question(question):
    data = ast.literal_eval(question)
    return data['id']


def get_response_id(question_id, sender_id):
    with db_connection.cursor() as cursor:
        sql = 'SELECT id from questions_given WHERE sender_id = %s AND question_id = %s ORDER BY time_asked LIMIT 1'
        cursor.execute(sql, (sender_id, question_id))
        return cursor.fetchone()['id']


def insert_user_answer(answer):
    with db_connection.cursor() as cursor:
        sql = 'INSERT INTO answer_provided (id, sender_id, question_id, answer, is_correct) VALUES (%s, %s, %s, %s, %s)'
        values = parse_answer(answer)
        response_id = get_response_id(values.question_id, values.sender_id)
        cursor.execute(sql, (response_id, values.sender_id, values.question_id, values.answer, values.is_correct))
    db_connection.commit()


def parse_answer(answer):
    data = ast.literal_eval(answer)
    return user_answer(
        sender_id=data['sender']['id'],
        question_id=ast.literal_eval(data['postback']['payload'])['qid'],
        answer=data['postback']['title'],
        is_correct=True if ast.literal_eval(data['postback']['payload'])['correct'] == ast.literal_eval(data['postback']['payload'])['id'] else False
        )
