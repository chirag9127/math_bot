from database.db_connection import execute_sql
from messenger_bot.logger import log


def questions_answered(sender_id, num):
    try:
        sql = "select count(*) from answer_provided where time_asked \
            BETWEEN (select CURRENT_TIMESTAMP + interval '-%s' day) \
            AND (select CURRENT_TIMESTAMP) \
            AND sender_id = %s"
        cursor = execute_sql(sql)
        response = cursor.fetchone()['count(*)']
        cursor.close()
        return response
    except:
        log('error! questions answered')
        return None


def questions_answered_today(sender_id):
    return questions_answered(sender_id, 1)


def questions_answered_last_week(sender_id):
    return questions_answered(sender_id, 7)


def questions_answered_last_month(sender_id):
    return questions_answered(sender_id, 30)


def questions_answered_correctly(sender_id, num):
    try:
        sql = "select count(*) from answer_provided where time_asked \
            BETWEEN (select CURRENT_TIMESTAMP + interval '-%s' day) \
            AND (select CURRENT_TIMESTAMP) \
            AND is_correct = 1 \
            AND sender_id = %s"
        cursor = execute_sql(sql)
        response = cursor.fetchone()['count(*)']
        cursor.close()
        return response
    except:
        log('error! questions answered correctly')
        return None


def questions_answered_correctly_today(sender_id):
    return questions_answered_correctly(sender_id, 1)


def questions_answered_correctly_last_week(sender_id):
    return questions_answered_correctly(sender_id, 7)


def questions_answered_correctly_last_month(sender_id):
    return questions_answered_correctly(sender_id, 30)


def score_in_given_topic(sender_id, topic):
    try:
        sql = "select count(*) \
            from answer_provided a join questions_question q \
            on q.id = a.question_id \
            where a.is_correct = 1 \
            AND q.topic = %s AND a.sender_id = %s"
        cursor = execute_sql(sql)
        response = cursor.fetchone()['count(*)']
        cursor.close()
        return response
    except:
        log('error! score in a given topic')
        return None


def top_two_scoring_topics(sender_id):
    try:
        sql = "select count(*), q.topic \
            from answer_provided a join questions_question q \
            on q.id = a.question_id \
            where a.is_correct = 1 AND a.sender_id = %s \
            GROUP BY q.topic \
            ORDER BY count(*) DESC \
            LIMIT 2"
        cursor = execute_sql(sql)
        res = cursor.fetchall()
        log(res)
        res = [r['topic'] for r in res]
        cursor.close()
        return res
    except:
        log('error! top two scoring topics')
        return None


def bottom_two_scoring_topics(sender_id):
    try:
        sql = "select count(*), q.topic \
            from answer_provided a join questions_question q \
            on q.id = a.question_id \
            where a.is_correct = 1 AND a.sender_id = %s \
            GROUP BY q.topic \
            ORDER BY count(*) \
            LIMIT 2"
        cursor = execute_sql(sql)
        res = cursor.fetchall()
        res = [r['topic'] for r in res]
        cursor.close()
        return res
    except:
        log('error! bottom two scoring topics')
        return None


def questions_grouped_by_date_last_week(sender_id):
    try:
        sql = "select DATE(time_asked) AS ForDate, count(*) \
                from answer_provided \
                where time_asked \
                BETWEEN (select CURRENT_TIMESTAMP + interval '-7' day) \
                AND (select CURRENT_TIMESTAMP) AND \
                sender_id = %s \
                GROUP BY ForDate"
        cursor = execute_sql(sql)
        response = cursor.fetchall()
        cursor.close()
        return response
    except:
        log('error! questions group by date')
        return None


def scores_in_topics(sender_id):
    try:
        sql = "select count(*), q.topic \
                from answer_provided a join questions_question q \
                on q.id = a.question_id \
                where a.is_correct = 1 AND a.sender_id = %s \
                GROUP BY q.topic \
                ORDER BY count(*) DESC"
        cursor = execute_sql(sql)
        response = cursor.fetchall()
        cursor.close()
        return response
    except:
        log('error! scores in topics')
        return None


def correct_questions_grouped_by_date_last_week(sender_id):
    try:
        sql = "select DATE(time_asked) AS ForDate, count(*) \
                from answer_provided \
                where time_asked \
                BETWEEN (select CURRENT_TIMESTAMP + interval '-7' day) \
                AND (select CURRENT_TIMESTAMP) AND is_correct = 1 AND \
                sender_id = %s\
                GROUP BY ForDate"
        cursor = execute_sql(sql)
        response = cursor.fetchall()
        cursor.close()
        return response
    except:
        log('error! correct questions group by date')
        return None


def questions_grouped_by_date_last_month(sender_id):
    try:
        sql = "select DATE(time_asked) AS ForDate, count(*) \
                from answer_provided \
                where time_asked \
                BETWEEN (select CURRENT_TIMESTAMP + interval '-30' day) \
                AND (select CURRENT_TIMESTAMP) AND \
                sender_id = %s \
                GROUP BY ForDate"
        cursor = execute_sql(sql)
        response = cursor.fetchall()
        cursor.close()
        return response
    except:
        log('error! questions group by date')
        return None


def correct_questions_grouped_by_date_last_month(sender_id):
    try:
        sql = "select DATE(time_asked) AS ForDate, count(*) \
                from answer_provided \
                where time_asked \
                BETWEEN (select CURRENT_TIMESTAMP + interval '-30' day) \
                AND (select CURRENT_TIMESTAMP) AND is_correct = 1 AND \
                sender_id = %s\
                GROUP BY ForDate"
        cursor = execute_sql(sql)
        response = cursor.fetchall()
        cursor.close()
        return response
    except:
        log('error! correct questions group by date')
        return None


def questions_grouped_by_date_eternity(sender_id):
    try:
        sql = "select DATE(time_asked) AS ForDate, count(*) \
                from answer_provided \
                where sender_id = %s \
                GROUP BY ForDate"
        cursor = execute_sql(sql)
        response = cursor.fetchall()
        cursor.close()
        return response
    except:
        log('error! questions group by date')
        return None


def correct_questions_grouped_by_date_eternity(sender_id):
    try:
        sql = "select DATE(time_asked) AS ForDate, count(*) \
                from answer_provided \
                where sender_id = %s AND \
                is_correct = 1 \
                GROUP BY ForDate"
        cursor = execute_sql(sql)
        response = cursor.fetchall()
        cursor.close()
        return response
    except:
        log('error! correct questions group by date')
        return None
