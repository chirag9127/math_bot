import os
import wolframalpha
from messenger_bot.logger import log
from configparser import ConfigParser


def get_wolfram_key():
    config = ConfigParser(os.environ)
    config.read('/dev/null')
    return os.environ['WOLFRAM_API_KEY']


def get_solution_gifs(question):
    API = get_wolfram_key()
    client = wolframalpha.Client(API)
    result = client.query(question)
    if not result or not result.pods:
        return None
    gifs = []
    try:
        for item in result.pods:
            if 'subpod' in item and isinstance(item['subpod'], list):
                for i in item['subpod']:
                    gifs.append(i['img']['@src'])
            elif 'subpod' in item and isinstance(item['subpod'], dict):
                gifs.append(item['subpod']['img']['@src'])
        return gifs
    except:
        log('unable to parse wolfram result')
