""" 
Summary: 
    Library which contains all the functions related to 
    the attendance (voting) part of the tool.
"""

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
    """Creates a pichart with the attendance of all users
    Returns:
        String: Returns a div that can be shown in the html
    """
    data = file_helper.read_all_weeks()

    count = {}
    for week in data: # Need to iterate all weeks saved
        for day in week['days']: # Need to interate over Mo - So in Week
            for person, attend in day.get('attending', {}).items():
                if attend:
                    count[person] = count.get(person, 0) + 1

    labels = [ k.capitalize() for k in count ] # Get all Labels a.k Names of Person
    values = [ v for v in count.values() ] # Get all values 

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    div = plot(fig, output_type="div")

    return div