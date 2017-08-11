import os
from operator import itemgetter
from messenger_bot.logger import log
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from database.diagnostic import (questions_grouped_by_date_last_week,
                                 correct_questions_grouped_by_date_last_week,
                                 questions_grouped_by_date_last_month,
                                 correct_questions_grouped_by_date_last_month,
                                 questions_grouped_by_date_eternity,
                                 correct_questions_grouped_by_date_eternity,
                                 scores_in_topics)
import numpy as np


def get_file_name(file_id):
    return os.getcwd()+'/database/images/score_{}.png'.format(file_id)


def delete_img(file_id):
    os.remove(get_file_name(file_id))


def answered_vs_correct_plot(
        file_id, title, question_color, x_axis=[0], y_axis_1=[0], y_axis_2=[0]):
    ind = np.arange(len(x_axis))
    width = 0.35
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, y_axis_2, width, color='lightgreen')
    rects2 = ax.bar(ind+width, y_axis_1, width, color=question_color)
    # add some text for labels, title and axes ticks
    ax.set_ylabel('Scores')
    ax.set_title(title)
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(tuple(x_axis))
    ax.legend((rects1[0], rects2[0]), ('Correct', 'Answered'))
    autolabel(ax, rects1)
    autolabel(ax, rects2)
    plt.savefig(get_file_name(file_id))


def scores_in_topics_plot(sender_id, file_id):
    try:
        data = scores_in_topics(sender_id)
        labels = [item['topic'] for item in data]
        sizes = [item['count(*)'] for item in data]
        labels = labels if len(labels) > 0 else [0]
        sizes = sizes if len(sizes) > 0 else [0]
        fig1, ax1 = plt.subplots()
        ax1.set_title('topic wise strengths')
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')
        plt.savefig(get_file_name(file_id))
    except:
        log('error! scores in topic')


def autolabel(ax, rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom')


def call_bar_plot(
        question_count, correct_count, file_id, title, question_color):
    try:
        x_axis = [item['ForDate'].strftime('%m/%d/%Y') for item in question_count]
        y_axis_1 = [item['count(*)'] for item in question_count]
        y_axis_2 = [item['count(*)'] for item in correct_count]
        x_axis = x_axis if len(x_axis) > 0 else [0]
        y_axis_1 = y_axis_1 if len(y_axis_1) > 0 else [0]
        y_axis_2 = y_axis_2 if len(y_axis_2) > 0 else [0]
        answered_vs_correct_plot(
            file_id, title, question_color, x_axis, y_axis_1, y_axis_2)
        return True
    except:
        log('unable to plot')
        return False


def plot_scores_for_last_week(sender_id, file_id):
    question_count = list(questions_grouped_by_date_last_week(sender_id))
    correct_count = list(correct_questions_grouped_by_date_last_week(sender_id))
    correct_count = polish_correct_count(question_count, correct_count)
    return call_bar_plot(
        question_count, correct_count, file_id, 'Progress over the week', 'lightcoral')


def plot_scores_for_last_month(sender_id, file_id):
    question_count = list(questions_grouped_by_date_last_month(sender_id))
    correct_count = list(correct_questions_grouped_by_date_last_month(sender_id))
    correct_count = polish_correct_count(question_count, correct_count)
    return call_bar_plot(
        question_count, correct_count, file_id, 'Progress over the month', 'royalblue')


def plot_scores_for_eternity(sender_id, file_id):
    question_count = list(questions_grouped_by_date_eternity(sender_id))
    correct_count = list(correct_questions_grouped_by_date_eternity(sender_id))
    correct_count = polish_correct_count(question_count, correct_count)
    return call_bar_plot(
        question_count, correct_count, file_id, 'Progress since you started', 'rosybrown')


def polish_correct_count(question_count, correct_count):
    correct_count_dates = [item['ForDate'] for item in correct_count]
    question_count_dates = [item['ForDate'] for item in question_count]
    for date in question_count_dates:
        if date not in correct_count_dates:
            correct_count.append({'ForDate': date, 'count(*)': 0})
    return sorted(correct_count, key=itemgetter('ForDate'))
