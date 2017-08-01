import ast
import os
import random

from messenger_bot.consts import *
from messenger_bot.logger import log
from messenger_bot.sender import send_text_message, send_image, \
    send_question, send_video
from database.db_api import question_from_topic, options_and_answer, \
    has_video, video


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
S3_LINK = os.environ['S3_LINK']


def handle_postback(event):
    log(event)
    sender_id = event['sender']['id']
    if 'postback' in event and 'payload' in event['postback']:
        payload = event['postback']['payload']
        payload = ast.literal_eval(payload)
        if 'test' in payload and payload['test'] is True:
            handle_test(payload, sender_id)
        elif 'first_message' in payload:
            handle_first_message(sender_id)
        else:
            handle_question(payload, sender_id)


def handle_first_message(sender_id):
    send_text_message(sender_id, 'My name is Noah, and I will be your '
                      'SAT Buddy to help you get your desired score!')
    send_happy_gif(sender_id)
    send_text_message(sender_id, 'To begin with, we would do a quick '
                      'assessment of your SAT concepts by asking you '
                      '4 questions at a time and then coach you on your '
                      'weak areas. :)')
    send_text_message(sender_id, 'Let me know when you are ready to start.')


def handle_test(payload, sender_id):
    if 'result' in payload:
        result = payload['result']
    else:
        result = []
    if payload['id'] == payload['correct']:
        result.append({'qid': payload['qid'], 'correct': True})
    else:
        result.append({'qid': payload['qid'], 'correct': False})
    remaining = payload['remaining']
    if remaining < 0:
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
    question_id = payload['qid']
    if payload['id'] == payload['correct']:
        send_text_message(sender_id, "That's the right answer!")
        send_image(sender_id, random.choice(correct_gifs))
    else:
        send_text_message(sender_id, "Sorry! That's not correct.")
        send_image(sender_id, random.choice(wrong_gifs))

    if has_video(question_id):
        send_text_message(
            sender_id, "Here's the video solution to the question")
        video_link = "{0}{1}".format(
            S3_LINK, video(question_id))
        send_video(sender_id, video_link)
