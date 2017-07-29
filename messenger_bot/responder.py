import json
import os
import requests
from messenger_bot.consts import *
from database.db_api import question_from_topic
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
        log(question_from_topic(topic))


def send_text_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(
        recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)
