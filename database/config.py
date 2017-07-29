import os
from configparser import ConfigParser
from collections import namedtuple

params = namedtuple('params', 'host, username, password, port')


def get_params():
    config = ConfigParser(os.environ)
    config.read('/dev/null')
    return params(
        host=os.environ['DB_HOST'],
        username=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'],
        port=3306)
