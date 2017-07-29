import json
import requests

from messenger_bot.api_ai import APIAI
from logger import log


def response(message_text, sender_id):
    response = APIAI.Instance().response(
        message_text, sender_id)
    log(response)
    if 'result' in response and 'fulfillment' \
            in response['result'] and 'speech' in \
            response['result']['fulfillment']:
        send_message(sender_id,
                        response['result']
                        ['fulfillment']['speech'])
    else:
        send_message(sender_id, 'roger that!')


def send_message(recipient_id, message_text):

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
