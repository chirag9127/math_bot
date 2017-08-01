import os
from uuid import uuid4
from flask import Flask, request
from database.insert import insert_user_request, insert_user_answer
from messenger_bot.logger import log
from messenger_bot.message_handler import handle_message
from messenger_bot.postback_handler import handle_postback
from messenger_bot.keyword_handler import is_keyword_query, handle_keyword

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and \
            request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == \
                os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    request_id = str(uuid4())
    insert_user_request(request_id, str(data))
    """
    you may not want to log every incoming message in production,
    but it's good for testing
    """

    if data["object"] == "page":

        for entry in data["entry"]:
            if 'messaging' in entry:
                for messaging_event in entry["messaging"]:
                    if messaging_event.get("message"):
                        sender_id = messaging_event["sender"]["id"]
                        # recipient_id = messaging_event["recipient"]["id"]
                        message_text = messaging_event["message"]["text"]
                        if is_keyword_query(message_text):
                            handle_keyword(sender_id, message_text)
                        else:
                            handle_message(message_text, sender_id, request_id)
                    if messaging_event.get("delivery"):  # delivery confirmation
                        pass

                    if messaging_event.get("optin"):  # optin confirmation
                        pass

                    if messaging_event.get("postback"):
                        insert_user_answer(str(messaging_event))
                        handle_postback(messaging_event)
                        log(messaging_event)

    return "ok", 200


if __name__ == '__main__':
    app.run(debug=True)
