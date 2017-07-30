import ast
import random

from messenger_bot.consts import *
from messenger_bot.logger import log
from messenger_bot.responder import send_text_message, send_image, \
    send_question
from database.db_api import question_from_topic, options_and_answer


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
        if 'test' in payload and payload['test'] is True:
            handle_test(payload, sender_id)
            if 'result' in payload:
                result = payload['payload']
            else:
                result = []
            if payload['id'] == payload['correct']:
                result.append({'qid': payload['qid'], 'correct': True})
            else:
                result.append({'qid': payload['qid'], 'correct': False})
            topics = payload['topics']
            question = question_from_topic(topics.pop())
            options = options_and_answer(question[ID])
            send_question(sender_id, question, options,
                          remaining=payload['remaining'] - 1,
                          topics=topics, diagnostic=True, test=True)
        else:
            handle_question(payload, sender_id)


def handle_test(payload, sender_id):
    if 'result' in payload:
        result = payload['payload']
    else:
        result = []
    if payload['id'] == payload['correct']:
        result.append({'qid': payload['qid'], 'correct': True})
    else:
        result.append({'qid': payload['qid'], 'correct': False})
    if remaining == 0:
        count_correct = sum([1 if res['correct'] else 0 for res in result])
        count_total = len(result)
        send_text_message(sender_id, "You got {0} out of {1}".format(
            count_correct, count_total
        ))
    else:
        topics = payload['topics']
        question = question_from_topic(topics.pop())
        options = options_and_answer(question[ID])
        send_question(sender_id, question, options,
                      remaining=payload['remaining'] - 1,
                      topics=topics, diagnostic=True, test=True, result=result)


def handle_question(payload, sender_id):
    if payload['id'] == payload['correct']:
        send_text_message(sender_id, "That's the right answer!")
        send_image(sender_id, random.choice(correct_gifs))
    else:
        send_text_message(sender_id, "Sorry! That's not correct.")
        send_image(sender_id, random.choice(wrong_gifs))
