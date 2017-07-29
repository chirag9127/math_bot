import os
from configparser import ConfigParser
from collections import namedtuple

params = namedtuple('params', 'host, username, password, port')


def get_params():
    config = ConfigParser(os.environ)
    config.read('/dev/null')
    return params(
        host=os.environ['HOST'],
        username=os.environ['USERNAME'],
        password=os.environ['PASSWORD'],
        port=3306)
