from database.db_connection import DBConnection
from collections import namedtuple
import ast

db_connection = DBConnection.Instance().get_connection()

user_request = namedtuple('user_request', 'id, query')

user_response = namedtuple('user_response', 'intent, entities, response, sender_id')


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


def insert_users_question(response_id, sender_id, question):
    pass


def parse_question(question):
    data = ast.literal_eval(question)
    return data['id']
