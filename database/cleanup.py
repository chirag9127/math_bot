from database.db_connection import DBConnection


db_connection = DBConnection.Instance().get_connection()

filters = {'<table>', '</table>', '<sup>', '</sup', '</div', '<sub>', '</sub>',
           '<span', '</script>', '</b>', '</p>', '</center>', '</ol>', '<li>',
           '<img', '</u>'}


def get_questions():
    cursor = db_connection.cursor()
    sql = 'SELECT id, question_text from questions_question where deleted= 0 ' \
        'and section = "Quant"'
    cursor.execute(sql)
    questions = [(item['id'], item['question_text'])
                 for item in cursor.fetchall()]
    for question in questions:
        if is_correct(question[1]):
            sql_2 = 'UPDATE questions_question SET correct=TRUE WHERE id = %s'
            cursor.execute(sql_2, (question[0]))
    db_connection.commit()


def get_options():
    cursor = db_connection.cursor()
    sql = 'SELECT o.id, o.qid_id, o.option_text from questions_option o ' \
        'join questions_question q on o.qid_id = q.id'
    cursor.execute(sql)
    for item in cursor.fetchall():
        if not is_correct(item['option_text']):
            sql_2 = 'UPDATE questions_question SET correct=FALSE WHERE id = %s'
            cursor.execute(sql_2, (item['qid_id']))
    db_connection.commit()


def is_correct(question):
    if any(fil in question for fil in filters):
        return False
    return True


if __name__ == "__main__":
    get_options()
