from database.db_connection import DBConnection


db_connection = DBConnection.Instance().get_connection()


def questions_answered(sender_id, num):
    with db_connection.cursor() as cursor:
        sql = "select count(*) from answer_provided where time_asked \
            BETWEEN (select CURRENT_TIMESTAMP + interval '-%s' day) \
            AND (select CURRENT_TIMESTAMP) \
            AND sender_id = %s"
        cursor.execute(sql, (num, sender_id))
        return cursor.fetchone()['count(*)']


def questions_answered_today(sender_id):
    return questions_answered(sender_id, 1)


def questions_answered_last_week(sender_id):
    return questions_answered(sender_id, 7)


def questions_answered_last_month(sender_id):
    return questions_answered(sender_id, 30)


def questions_answered_correctly(sender_id, num):
    with db_connection.cursor() as cursor:
        sql = "select count(*) from answer_provided where time_asked \
            BETWEEN (select CURRENT_TIMESTAMP + interval '-%s' day) \
            AND (select CURRENT_TIMESTAMP) \
            AND is_correct = 1 \
            AND sender_id = %s"
        cursor.execute(sql, (num, sender_id))
        return cursor.fetchone()['count(*)']


def questions_answered_correctly_today(sender_id):
    return questions_answered_correctly(sender_id, 1)


def questions_answered_correctly_last_week(sender_id):
    return questions_answered_correctly(sender_id, 7)


def questions_answered_correctly_last_month(sender_id):
    return questions_answered_correctly(sender_id, 30)


def score_in_given_topic(sender_id, topic):
    with db_connection.cursor() as cursor:
        sql = "select count(*) \
            from answer_provided a join questions_question q \
            on q.id = a.question_id \
            where a.is_correct = 1 \
            AND q.topic = %s AND a.sender_id = %s"
        cursor.execute(sql, (topic, sender_id))
        return cursor.fetchone()['count(*)']


def top_two_scoring_topics(sender_id):
    with db_connection.cursor() as cursor:
        sql = "select count(*), q.topic \
            from answer_provided a join questions_question q \
            on q.id = a.question_id \
            where a.is_correct = 1 AND a.sender_id = %s \
            GROUP BY q.topic \
            ORDER BY count(*) DESC \
            LIMIT 2"
        cursor.execute(sql, (sender_id))
        res = cursor.fetchall()
        return [r['topic'] for r in res]


def bottom_two_scoring_topics(sender_id):
    with db_connection.cursor() as cursor:
        sql = "select count(*), q.topic \
            from answer_provided a join questions_question q \
            on q.id = a.question_id \
            where a.is_correct = 1 AND a.sender_id = %s \
            GROUP BY q.topic \
            ORDER BY count(*) \
            LIMIT 2"
        cursor.execute(sql, (sender_id))
        return cursor.fetchall()


def questions_grouped_by_date_last_week(sender_id):
    try:
        with db_connection.cursor() as cursor:
            sql = "select DATE(time_asked) AS ForDate, count(*) \
                    from answer_provided \
                    where time_asked \
                    BETWEEN (select CURRENT_TIMESTAMP + interval '-7' day) \
                    AND (select CURRENT_TIMESTAMP) AND \
                    sender_id = %s \
                    GROUP BY ForDate"
            cursor.execute(sql, (sender_id))
            return cursor.fetchall()
    except:
        log('error! questions group by date')


def correct_questions_grouped_by_date_last_week(sender_id):
    try:
        with db_connection.cursor() as cursor:
            sql = "select DATE(time_asked) AS ForDate, count(*) \
                    from answer_provided \
                    where time_asked \
                    BETWEEN (select CURRENT_TIMESTAMP + interval '-7' day) \
                    AND (select CURRENT_TIMESTAMP) AND is_correct = 1 AND \
                    sender_id = %s\
                    GROUP BY ForDate"
            cursor.execute(sql, (sender_id))
            return cursor.fetchall()
    except:

        log('error! correct questions group by date')
