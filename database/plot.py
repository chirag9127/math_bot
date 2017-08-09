import os
import plotly.plotly as py
import plotly.graph_objs as go
from configparser import ConfigParser
from database.diagnostic import (questions_grouped_by_date_last_week,
                                 correct_questions_grouped_by_date_last_week)

config = ConfigParser(os.environ)
config.read('/dev/null')
py.sign_in(os.environ['PLOTLY_USER'], os.environ['PLOTLY_API_KEY'])


def save_img(fig, file_id):
    py.image.save_as(fig, filename=get_file_name(file_id))


def get_file_name(file_id):
        return os.getcwd()+'/database/images/score_{}.jpeg'.format(file_id)


def delete_img(file_id):
    os.remove(get_file_name(file_id))


def plot(x_axis, y_axis_1, y_axis_2):
    trace1 = go.Bar(
        x=x_axis,
        y=y_axis_1,
        name='Questions Answered',
        marker=dict(
            color='rgb(126,14, 122)'
            )
        )
    trace2 = go.Bar(
        x=x_axis,
        y=y_axis_2,
        name='Correct',
        marker=dict(
            color='rgb(135, 194, 141)'
            )
    )
    data = [trace1, trace2]
    layout = go.Layout(
        barmode='group'
    )
    fig = go.Figure(data=data, layout=layout)
    return fig


def plot_scores_for_last_week(sender_id, file_id):
    question_count = questions_grouped_by_date_last_week(sender_id)
    correct_count = correct_questions_grouped_by_date_last_week(sender_id)
    x_axis = [item['ForDate'].strftime('%m/%d/%Y') for item in question_count]
    y_axis_1 = [item['count(*)'] for item in question_count]
    y_axis_2 = [item['count(*)'] for item in correct_count]
    fig = plot(x_axis, y_axis_1, y_axis_2)
    save_img(fig, file_id)
