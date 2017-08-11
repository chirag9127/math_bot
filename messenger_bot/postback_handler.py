import ast
import os
import random
from uuid import uuid4

from messenger_bot.consts import *
from messenger_bot.logger import log
from messenger_bot.sender import send_text_message, send_image, \
    send_question, send_video, send_happy_gif, send_helper_messages
from messenger_bot.api_ai import APIAI
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


def handle_postback(event, sender_id, request_id):
    log(event)
    if 'postback' in event and 'payload' in event['postback']:
        payload = event['postback']['payload']
        payload = ast.literal_eval(payload)
        if 'type' in payload and payload['type'] == 'num_questions':
            handle_new_test(payload, sender_id, request_id)
        elif 'test' in payload and payload['test'] is True:
            handle_test(payload, sender_id, request_id)
        elif 'first_message' in payload:
            handle_first_message(sender_id)
        else:
            handle_question(payload, sender_id)


def handle_new_test(payload, sender_id, request_id):
    test_id = str(uuid4())
    topic = payload['topic']
    num = int(payload['num'])
    if topic.strip() == '':
        question = question_from_topic('Arithmetic')
        options = options_and_answer(question[ID])
        send_question(sender_id, request_id, question, options,
                      remaining=num - 2,
                      topics=['Algebra', 'Geometry',
                              'Word Problems', 'Statistics'],
                      diagnostic=False, test=True, topic='Arithmetic',
                      test_id=test_id)
    else:
        question = question_from_topic(topic)
        options = options_and_answer(question[ID])
        send_question(sender_id, request_id, question, options,
                      remaining=num - 2,
                      topics=[topic] * 4,
                      diagnostic=False, test=True, topic=topic,
                      test_id=test_id)


def handle_first_message(sender_id):
    APIAI.Instance().event_response("getting_started_event", sender_id)
    send_text_message(sender_id, "Hi! My name is Noah! I'm here to help you "
                                 "prepare well for SAT maths. ")
    send_happy_gif(sender_id)
    send_text_message(sender_id,
                      "You can ask me to do any of the following: \r\n"
                      "- Take a quick test \r\n"
                      "- Watch a youtube video explaining the concept like "
                      "algebra, geometry, etc.\r\n"
                      "- practice some questions\r\n"
                      "- Ask us to solve polynomial function equations\r\n"
                      "- See a graph of your progress on diagnostic tests")
    """
    send_text_message(sender_id, 'To begin with, we would do a quick '
                      'assessment of your SAT Math concepts by asking you '
                      '5 questions to understand your strengths '
                      'and weaknesses :)')
    """
    send_text_message(sender_id, "Do you want to do a diagnostic test?")
    send_text_message(sender_id, "Type 'Yes' to go ahead with the test.")


def handle_test(payload, sender_id, request_id):
    if 'result' in payload:
        result = payload['result']
    else:
        result = []
    if payload['id'] == payload['correct']:
        result.append({'qid': payload['qid'], 'correct': True})
    else:
        result.append({'qid': payload['qid'], 'correct': False})
    test_id = payload['test_id']
    remaining = payload['remaining']
    if remaining < 0:
        count_correct = sum([1 if res['correct'] else 0 for res in result])
        count_total = len(result)
        send_text_message(sender_id, "You got {0} out of {1}".format(
            count_correct, count_total
        ))
        send_helper_messages(sender_id)
    else:
        topics = payload['topics']
        question = question_from_topic(topics.pop())
        options = options_and_answer(question[ID])
        send_question(sender_id, request_id, question, options,
                      remaining=payload['remaining'] - 1,
                      topics=topics, diagnostic=True, test=True, result=result,
                      test_id=test_id)


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
    send_helper_messages(sender_id)
