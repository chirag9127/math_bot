import ast
import random

from messenger_bot.logger import log
from messenger_bot.responder import send_text_message, send_image


correct_gifs = [
    'https://media.giphy.com/media/3oGRFp0AqM0BY4axjO/giphy.gif',
    'https://media.giphy.com/media/j2PS9MGm85WkE/giphy.gif',
    'https://media.giphy.com/media/26tknCqiJrBQG6bxC/giphy.gif',
]
wrong_gifs = [
    'https://media.giphy.com/media/hPPx8yk3Bmqys/giphy.gif',
    'https://media.giphy.com/media/BPZenX37AtXyw/giphy.gif',
    'https://media.giphy.com/media/l4pLY0zySvluEvr0c/giphy.gif',
]


def handle(event):
    log(event)
    sender_id = event['sender']['id']
    if 'postback' in event and 'payload' in event['postback']:
        payload = event['postback']['payload']
        payload = ast.literal_eval(payload)
        if payload['id'] == payload['correct']:
            send_text_message(sender_id, "That's the right answer!")
            send_image(sender_id, random.choice(correct_gifs))
        else:
            send_text_message(sender_id, "Sorry! That's not correct.")
            send_image(sender_id, random.choice(wrong_gifs))
