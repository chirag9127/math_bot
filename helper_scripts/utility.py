from collections import namedtuple


def enum(**keys):
    return namedtuple('Enum', keys)(**keys)


def filter_question(question):
    if not question.strip():
        None
    for token in ['<br/>', '</i>', '<i>', '<br>', '<em>', '</em>', '<br />', '<br />']:
        question = question.replace(token, '')
    question = question.replace('&gt;', '>').replace('&lt;', '<')
    return question
