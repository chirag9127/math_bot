from messenger_bot.consts import *
from database.db_api import question_from_topic, options_and_answer
from database.diagnostic import questions_answered_today, \
    questions_answered_last_week, questions_answered_last_month, \
    questions_answered_correctly_today, \
    questions_answered_correctly_last_week, \
    questions_answered_correctly_last_month, top_two_scoring_topics, \
    bottom_two_scoring_topics
from database.plot import plot_scores_for_last_week, delete_img, get_file_name
from messenger_bot.api_ai import APIAI
from messenger_bot.logger import log
from messenger_bot.sender import send_text_message, send_question, \
    send_helper_messages, send_open_graph_video, send_num_questions, \
    send_image_local
from search.youtube_search import get_most_relevant_video
from uuid import uuid4


def handle_message(message_text, sender_id, request_id):
    response = APIAI.Instance().message_response(
        message_text, sender_id)
    intent = response[RESULT][METADATA][INTENT_NAME]
    # insert_user_response(request_id, str(response))
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
    elif intent == TEST:
        test_start_flow(sender_id, response)
    elif intent == QUESTIONS_ANSWERED:
        questions_answered_flow(sender_id, response)
    elif intent == QUESTIONS_ANSWERED_CORRECTLY:
        questions_answered_correctly_flow(sender_id, response)
    elif intent == TOP_TOPICS:
        top_topics_flow(sender_id)
    elif intent == BOTTOM_TOPICS:
        bottom_topics_flow(sender_id)
    elif intent == PLOT_SCORES:
        plot_scores_flow(sender_id)
    elif intent == DEFAULT:
        send_text_message(sender_id,
                          response[RESULT][FULFILLMENT][SPEECH])
        send_helper_messages(sender_id)


def plot_scores_flow(sender_id):
    img_id = str(uuid4())
    plot_scores_for_last_week(sender_id, img_id)
    image_path = get_file_name(img_id)
    send_image_local(sender_id, image_path)
    delete_img(img_id)


def top_topics_flow(sender_id):
    top_topics = top_two_scoring_topics(sender_id)
    send_text_message(
        sender_id, 'Your strengths are {}'.format(', '.join(top_topics)))


def bottom_topics_flow(sender_id):
    bottom_topics = bottom_two_scoring_topics(sender_id)
    send_text_message(
        sender_id, 'Your weaknesses are {}'.format(', '.join(bottom_topics)))


def questions_answered_correctly_flow(sender_id, response):
    time_periods = response[RESULT][PARAMETERS][TIME_PERIODS]
    if time_periods == '' or time_periods.lower() == 'today':
        time_periods = 'today'
        questions_answered = questions_answered_correctly_today(sender_id)
    elif time_periods.lower() == 'last month':
        time_periods = 'last month'
        questions_answered = questions_answered_correctly_last_month(sender_id)
    elif time_periods.lower() == 'last week':
        time_periods = 'last week'
        questions_answered = questions_answered_correctly_last_week(sender_id)
    send_text_message(
        sender_id, 'You have answered {0} questions correctly {1}'.format(
            questions_answered, time_periods))


def questions_answered_flow(sender_id, response):
    time_periods = response[RESULT][PARAMETERS][TIME_PERIODS]
    if time_periods == '' or time_periods.lower() == 'today':
        time_periods = 'today'
        questions_answered = questions_answered_today(sender_id)
    elif time_periods.lower() == 'last month':
        time_periods = 'last month'
        questions_answered = questions_answered_last_month(sender_id)
    elif time_periods.lower() == 'last week':
        time_periods = 'last week'
        questions_answered = questions_answered_last_week(sender_id)
    send_text_message(sender_id, 'You have answered {0} questions {1}'.format(
        questions_answered, time_periods))
    send_helper_messages(sender_id)


def test_start_flow(sender_id, response):
    topic = response[RESULT][PARAMETERS][TOPICS]
    send_num_questions(
        sender_id, response[RESULT][FULFILLMENT][SPEECH], topic)
    send_helper_messages(sender_id)


def video_flow(sender_id, message_text):
    most_relevant_video = get_most_relevant_video(message_text)
    video_link = 'https://www.youtube.com/watch?v={}'.format(
        most_relevant_video)
    send_text_message(sender_id, 'Here is a video on this:')
    send_open_graph_video(sender_id, video_link)
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
    topic = response[RESULT][PARAMETERS][TOPICS]
    if topic != 'default_topic':
        send_text_message(sender_id, response[RESULT][FULFILLMENT][SPEECH])
    else:
        topic = ''
        send_text_message(sender_id, "Sure! Let's start with this:")
    log("TOPIC: {}".format(topic))
    question = question_from_topic(topic)
    options = options_and_answer(question[ID])
    send_question(sender_id, request_id, question, options, topic=topic)
