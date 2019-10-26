from . import week_date_helper
from . import data_helper
from . import week_data_handler
from . import data_helper

import datetime

def vote(attending, date, person):
    date = datetime.datetime.strptime(date, '%d%m%Y')
    week = week_date_helper.calculate_week_from_date(date)
    week_data = week_data_handler.load_week(week[0], week[1])

    for day in week_data['days']:
        if (day.get('date') == date.strftime("%d.%m.%Y")):
            day['attending'][person.lower()] = attending
    
    data_helper.save_json(week_data_handler.get_file_path(week[0], week[1]), week_data)