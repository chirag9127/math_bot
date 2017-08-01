import os
import json
import requests


def set_greeting():
    data = json.dumps({
        "greeting": [
                {
                    "locale": "default",
                    "text": "Hi {{user_first_name}}! Welcome to SATBuddy!.",
                }
        ]
    })
    send(data)


def set_getting_started():
    data = json.dumps({
        "get_started": {
            "payload": str({"first_message": "first_message"}),
        }
    })
    send(data)


def send(data):
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    r = requests.post("https://graph.facebook.com/v2.6/me/messenger_profile",
                      params=params, headers=headers, data=data)
    if r.status_code != 200:
        print (r.status_code)
        print (r.text)


if __name__ == "__main__":
    set_getting_started()
