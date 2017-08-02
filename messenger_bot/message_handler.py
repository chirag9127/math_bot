from messenger_bot.consts import *
from database.db_api import question_from_topic, options_and_answer
from messenger_bot.api_ai import APIAI
from messenger_bot.logger import log
from messenger_bot.sender import send_text_message, send_question, \
    send_helper_messages, send_video
from search.youtube_search import get_most_relevant_video
from uuid import uuid4


def handle_message(message_text, sender_id, request_id):
    response = APIAI.Instance().message_response(
        message_text, sender_id)
    intent = response[RESULT][METADATA][INTENT_NAME]
    #insert_user_response(request_id, str(response))
    log(response)
    if intent == STUDY:
        study_flow(sender_id, response, request_id)
    elif intent == GREETING:
        greeting_flow(sender_id, response)
    elif intent == DIAGNOSTIC_NO:
        diagnostic_no_flow(sender_id, response)
    elif intent == DIAGNOSTIC_YES:
        diagnostic_yes_flow(sender_id, response, request_id)
    elif intent == VIDEO_SEARCH:
        video_flow(sender_id, message_text)
    elif intent == DEFAULT:
        send_text_message(sender_id,
                          response[RESULT][FULFILLMENT][SPEECH])
        send_helper_messages(sender_id)


def video_flow(sender_id, message_text):
    most_relevant_video = get_most_relevant_video(message_text)
    video_link = 'https://www.youtube.com/watch?v={}'.format(
        most_relevant_video)
    send_text_message(sender_id, 'Here is a video on this:')
    send_video(sender_id, video_link)
    send_helper_messages(sender_id)


def diagnostic_yes_flow(sender_id, response, request_id):
    test_id = str(uuid4())
    send_text_message(sender_id, response[RESULT][FULFILLMENT][SPEECH])
    question = question_from_topic('Arithmetic')
    options = options_and_answer(question[ID])
    send_question(sender_id, request_id, question, options,
                  remaining=3, topics=['Algebra', 'Geometry',
                                       'Word Problems', 'Statistics'],
                  diagnostic=True, test=True, topic='Arithmetic',
                  test_id=test_id)


def diagnostic_no_flow(sender_id, response):
    send_text_message(sender_id, response[RESULT][FULFILLMENT][SPEECH])
    send_helper_messages(sender_id)


def greeting_flow(sender_id, response):
    send_text_message(sender_id, 'Hi! How are you doing today? '
                                 'Here is what we can help you with:')
    send_helper_messages(sender_id)


def study_flow(sender_id, response, request_id):
    send_text_message(sender_id, response[RESULT][FULFILLMENT][SPEECH])
    topic = response[RESULT][PARAMETERS][TOPICS]
    question = question_from_topic(topic)
    options = options_and_answer(question[ID])
    send_question(sender_id, request_id, question, options, topic=topic)
