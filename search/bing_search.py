import os
import http.client
import urllib.request
import urllib.parse
import urllib.error

from helper_scripts.construct_sentences import correct


SUBSCRIPTION_KEY = os.environ['BING_SUBSCRIPTION_KEY']


class BingSearcher:

    def __init__(self):
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY,
        }
        self.params = urllib.parse.urlencode({
            'mode': 'proof',
            'mkt': 'en-us',
        })

    def get_response(self, query):
        try:
            query = 'Text={}'.format('+'.join(query.split()))
            conn = http.client.HTTPSConnection('api.cognitive.microsoft.com')
            conn.request("POST", "/bing/v5.0/spellcheck/?%s" % self.params,
                         query, self.headers)
            response = conn.getresponse()
            data = response.read()
            conn.close()
            return data
        except Exception:
            return None

    def __parse_and_correct(self, query, bing_response):
        response = eval(bing_response)
        corrections = []
        for flagged_tokens in response['flaggedTokens']:
            corrections.append(
                (flagged_tokens['offset'],
                 flagged_tokens['suggestions'][0]['suggestion']))
        corrected_sentence = correct(query, corrections)
        return corrected_sentence

    def correct_spelling(self, query):
        response = self.get_response(query)
        if not response:
            return query
        return self.__parse_and_correct(query, response)
