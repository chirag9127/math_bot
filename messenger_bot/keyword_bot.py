from search.wolfram_api import get_solution_gifs
from messenger_bot.responder import send_image, \
    send_text_message


def is_keyword_query(message_text):
    if message_text.starts_with('Solve:'):
        return True
    return False


def keyword_response(sender_id, message_text):
    question = message_text[6:]
    solution_gifs = get_solution_gifs(question)
    if solution_gifs:
        send_text_message(
            sender_id, "Here's your solution")
        for gif in solution_gifs:
            send_image(
                sender_id, gif)
