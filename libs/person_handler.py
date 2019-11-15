from . import date_helper
from . import week_handler
from . import file_helper

from plotly.offline import plot
import plotly.graph_objects as go

import datetime

def vote(attending, date, person):
    """Summary returns the file name for the file of a week
    Args:
        data_path (String): Folder where data is stored
        year (String): Year of weeknumber
        week_number (String):  Corrected number of week, first week = 1
    Returns:
        String: Returns the file path to a week file
    """
    date = datetime.datetime.strptime(date, '%d%m%Y')
    week = date_helper.calculate_week_from_date(date)
    week_data = week_handler.load_week(week[0], week[1])

    for day in week_data['days']:
        if (day.get('date') == date.strftime("%d.%m.%Y")):
            person_dict = day.get('attending', {})
            person_dict[person.lower()] = attending
            day['attending'] = person_dict

    file_helper.save_json(week_handler.get_file_path(week[0], week[1]), week_data)

def summary():
    data = file_helper.read_all_weeks()

    count = {}
    for week in data:
        for day in week['days']:
            for person, attend in day.get('attending', {}).items():
                if attend:
                    count[person] = count.get(person, 0) + 1

    labels = [ k.capitalize() for k in count ]
    values = [ v for v in count.values() ]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    div = plot(fig, output_type="div")

    return div