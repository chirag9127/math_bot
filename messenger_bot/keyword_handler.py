from search.wolfram_api import get_solution_gifs
from messenger_bot.sender import send_image, send_text_message, \
    send_helper_messages, send_open_graph_video
from search.youtube_search import get_most_relevant_video


def is_keyword_query(message_text):
    if message_text.lower().startswith('solve'):
        return True
    elif message_text.startswith('Video Search:'):
        return True
    return False


def handle_keyword(sender_id, message_text):
    if message_text.lower().startswith('solve'):
        handle_solver(sender_id, message_text)
    elif message_text.startswith('Video Search:'):
        handle_video_search(sender_id, message_text)


def handle_video_search(sender_id, message_text):
    message_text = message_text[13:]
    most_relevant_video = get_most_relevant_video(message_text)
    if most_relevant_video:
        video_link = 'https://www.youtube.com/watch?v={}'.format(
            most_relevant_video)
        send_text_message(sender_id, 'Here is a video on this:')
        send_open_graph_video(sender_id, video_link)
        send_helper_messages(sender_id)
    else:
        send_text_message(sender_id, 'Sorry! We could not find a video '
                                     'for the topic')


def handle_solver(sender_id, message_text):
    question = message_text[5:].strip()
    solution_gifs = get_solution_gifs(question)
    if solution_gifs:
        send_text_message(
            sender_id, "Here's your solution")
        for gif in solution_gifs:
            send_image(
                sender_id, gif)
    else:
        send_text_message(
            sender_id,
            "Sorry! We can't understand this question."
            "Will get back to you in a few days.")
    send_helper_messages(sender_id)
