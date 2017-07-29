import json
import os

import apiai

from util.singleton import Singleton


CLIENT_ACCESS_TOKEN = os.environ["CLIENT_ACCESS_TOKEN"]


@Singleton
class APIResponder(object):

    def __init__(self):
        self.ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

    def response(self, query, sender_id):
        request = self.ai.text_request()
        request.session_id = sender_id
        request.query = query
        response = request.getresponse()
        response = response.read()
        response = json.loads(response)
        return response
