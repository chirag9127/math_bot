from search.wolfram_api import get_solution_gifs
from messenger_bot.sender import send_image, send_text_message, \
    send_helper_messages


def is_keyword_query(message_text):
    if message_text.startswith('Solve:'):
        return True
    return False


def handle_keyword(sender_id, message_text):
    question = message_text[6:]
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
