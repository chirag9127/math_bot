import os
import json
import requests


def set_greeting():
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "greeting": [
                {
                    "locale": "default",
                    "text": "Hi {{user_first_name}}! Welcome to SATBuddy!.",
                }
        ]
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messenger_profile",
                      params=params, headers=headers, data=data)
    print (r.status_code)
    print (r.text)
    print (r)


if __name__ == "__main__":
    set_greeting()
