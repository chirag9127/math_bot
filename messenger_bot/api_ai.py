import json
import os

import apiai

from helper_scripts.singleton import Singleton


CLIENT_ACCESS_TOKEN = os.environ["CLIENT_ACCESS_TOKEN"]


@Singleton
class APIAI(object):

    def __init__(self):
        self.ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

    def message_response(self, query, sender_id):
        request = self.ai.text_request()
        request.session_id = sender_id
        request.query = query
        return self.__handle_response(request)

    def event_response(self, event_name, sender_id):
        request = self.ai.event_request(
            apiai.events.Event(event_name))
        request.session_id = sender_id
        return self.__handle_response(request)

    def __handle_response(self, request):
        response = request.getresponse()
        response = response.read()
        response = json.loads(response)
        return response
