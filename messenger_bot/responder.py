import json
import os
import requests

from messenger_bot.consts import *
from database.db_api import question_from_topic, options_and_answer
from messenger_bot.api_ai import APIAI
from messenger_bot.logger import log


def response(message_text, sender_id):
    response = APIAI.Instance().response(
        message_text, sender_id)
    intent = response[RESULT][METADATA][INTENT_NAME]
    log(response)
    if intent == STUDY:
        send_text_message(sender_id, response[RESULT][FULFILLMENT][SPEECH])
        topic = response[RESULT][PARAMETERS][TOPICS]
        question = question_from_topic(topic)
        options = options_and_answer(question[ID])
        log(question)
        log(options)
        send_question(sender_id, question)


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


def send_question(recipient_id, question):
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": question['question_text'],
                    "buttons": [
                        {
                            "type": "web_url",
                            "url": "https://petersapparel.parseapp.com",
                            "title": "Show Website"
                        },
                        {
                            "type": "postback",
                            "title": "Start Chatting",
                            "payload": "USER_DEFINED_PAYLOAD"
                        }
                    ]
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
