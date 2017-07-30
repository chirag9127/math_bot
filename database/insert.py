from database.db_connection import DBConnection
from collections import namedtuple
import ast

db_connection = DBConnection.Instance().get_connection()

user_request = namedtuple('user_request', 'id, query')

user_response = namedtuple('user_response', 'intent, entities, response, action')


def insert_user_request(request_id, request):
    with db_connection.cursor() as cursor:
        sql = 'INSERT INTO user_request (id, sender_id, query) VALUES (%s, %s, %s)'
        values = parse_request_data(request)
        cursor.execute(sql, (request_id, values.id, values.query))
    db_connection.commit()


def parse_request_data(request):
    data = ast.literal_eval(request)
    return user_request(
        id=data['entry'][0]['messaging'][0]['sender']['id'],
        query=data['entry'][0]['messaging'][0]['message']['text']
        )


def insert_user_response(response):
    with db_connection.cursor() as cursor:
        sql_to_request = 'INSERT INTO user_request (intent, entities) VALUES (%s, %s)'
        values = parse_response_data(request)
        cursor.execute(sql_to_request, (values.intent, values.entities))
        sql_to_response = 'INSERT INTO user_response (response, action) VALUES (%s, %s)'
        cursor.execute(sql_to_response, (values.response, values.action))
    db_connection.commit()


def parse_response_data(request):
    pass