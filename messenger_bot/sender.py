import json
import os
import random
import requests
from uuid import uuid4
from helper_scripts.utility import filter_question
from messenger_bot.consts import *
from messenger_bot.logger import log
from database.insert import insert_user_question


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


def send_video(recipient_id, video_link):
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type": "video",
                "payload": {
                    "url": video_link,
                }
            }
        }
    })
    send(data)


def send_open_graph_video(recipient_id, video_link):
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "open_graph",
                    "elements": [
                        {
                            "url": video_link,
                        }
                    ]
                }
            }
        }
    })
    send(data)


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


def send_question(recipient_id, request_id, question, options, **kwargs):
    log(question)
    #insert_user_question(request_id, recipient_id, str(question))
    buttons = []
    question_request_id = str(uuid4())
    for option in options.options:
        payload = {
            'id': option['id'],
            'correct': options.correct,
            'qid': question['id'],
            'question_request_id': question_request_id,
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


def send_helper_messages(sender_id):
    send_text_message(sender_id, "You can Practice questions by typing "
                                 "something like "
                                 "'I want to do a question on Algebra'")
    send_text_message(sender_id, "If you have a question you want the solution "
                                 "you can type 'Solve: x^2 - 1 = 0'")


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
