import os
import wolframalpha
from configparser import ConfigParser


def get_wolfram_key():
    config = ConfigParser(os.environ)
    config.read('/dev/null')
    return os.environ['WOLFRAM_API_KEY']


def get_solution_gifs(question):
    API = get_wolfram_key()
    client = wolframalpha.Client(API)
    result = client.query(question)
    return [pod['subpod']['img']['@src'] for pod in result.pods]
