import json
import os
import random
import requests

from helper_scripts.utility import filter_question
from messenger_bot.consts import *
from database.db_api import question_from_topic, options_and_answer
from messenger_bot.api_ai import APIAI
from messenger_bot.logger import log
from database.insert import insert_user_response


def response(message_text, sender_id, request_id):
    response = APIAI.Instance().response(
        message_text, sender_id)
    intent = response[RESULT][METADATA][INTENT_NAME]
    insert_user_response(request_id, str(response))
    log(response)
    if intent == STUDY:
        study_flow(sender_id, response)
    elif intent == GREETING:
        greeting_flow(sender_id, response)
    elif intent == DIAGNOSTIC_NO:
        diagnostic_no_flow(sender_id, response)
    elif intent == DIAGNOSTIC_YES:
        diagnostic_yes_flow(sender_id, response)
    else:
        send_text_message(sender_id,
                          response[RESULT][FULFILLMENT][SPEECH])


def diagnostic_yes_flow(sender_id, response):
    send_text_message(sender_id, response[RESULT][FULFILLMENT][SPEECH])
    question = question_from_topic('Arithmetic')
    options = options_and_answer(question[ID])
    send_question(sender_id, question, options,
                  remaining=3, topics=['Algebra', 'Geometry',
                                       'Word Problems', 'Statistics'],
                  diagnostic=True, test=True)


def diagnostic_no_flow(sender_id, response):
    send_text_message(sender_id, response[RESULT][FULFILLMENT][SPEECH])
    send_text_message(sender_id, 'Practice questions')
    send_text_message(sender_id, 'Do tests')
    send_text_message(sender_id, 'Watch Youtube Video explaining concept')
    send_text_message(sender_id, 'Ask us to solve a question')


def greeting_flow(sender_id, response):
    send_text_message(sender_id, response[RESULT][FULFILLMENT][SPEECH])
    send_happy_gif(sender_id)
    send_text_message(sender_id, 'My name is Noah, and I will be your '
                      'SAT Buddy to help you get your desired score!')
    send_text_message(sender_id, 'To begin with, we would do a quick '
                      'assessment of your SAT concepts by asking you '
                      '4 questions at a time and then coach you on your '
                      'weak areas. :)')
    send_text_message(sender_id, 'Let me know when you are ready to start.')


def send_happy_gif(sender_id):
    happy_gifs = [
        'https://media.giphy.com/media/DYH297XiCS2Ck/giphy.gif',
        'https://media.giphy.com/media/3oz8xRF0v9WMAUVLNK/giphy.gif',
        'https://media.giphy.com/media/11sBLVxNs7v6WA/giphy.gif',
    ]
    send_image(sender_id, random.choice(happy_gifs))


def send_image(recipient_id, image_link):
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": image_link,
                }
            }
        }
    })
    send(data)


def study_flow(sender_id, response):
    send_text_message(sender_id, response[RESULT][FULFILLMENT][SPEECH])
    topic = response[RESULT][PARAMETERS][TOPICS]
    question = question_from_topic(topic)
    options = options_and_answer(question[ID])
    send_question(sender_id, question, options)


def send(data):
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def send_question(recipient_id, question, options, **kwargs):
    log(question)
    buttons = []
    for option in options.options:
        payload = {
            'id': option['id'],
            'correct': options.correct,
            'qid': question['id']
        }
        payload.update(kwargs)
        payload = str(payload)
        button = {
            "type": "postback",
            "title": option['text'],
            "payload": payload,
        }
        buttons.append(button)
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": filter_question(question['question_text']),
                    "buttons": buttons,
                }
            }
        }
    })
    send(data)


def send_text_message(recipient_id, message_text):
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    send(data)
