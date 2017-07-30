from database.db_connection import DBConnection


db_connection = DBConnection.Instance().get_connection()

filters = {'<table>', '</table>', '<sup>', '</sup', '</div', '<sub>', '</sub>', '<span', '</script>',
                '</b>', '</p>', '</center>', '</ol>', '<li>', '<img', '</u>'}


def get_questions():
    cursor = db_connection.cursor()
    sql = 'SELECT id, question_text from questions_question where deleted=0 and section = "Quant"'
    cursor.execute(sql)
    questions = [(item['id'], item['question_text']) for item in cursor.fetchall()]
    for question in questions:
        if is_correct(question[1]):
            sql_2 = 'UPDATE questions_question SET correct=TRUE WHERE id = %s'
            cursor.execute(sql_2, (question[0]))
    db_connection.commit()


def is_correct(question):
    if any(fil in question for fil in filters):
        return False
    return True

if __name__ == "__main__":
    get_questions()



