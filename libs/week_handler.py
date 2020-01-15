""" 
Summary: 
    Library with functions for the week management
"""

from . import file_helper
from . import week_handler
from . import date_helper
from . import config

def load_week(year, week_number):
    """Summary Loads the specified week data, if week not created yet it creates
    an empty week.
    Args:
        year (String): Year of of weeknumber
        week_number (String): Corrected number of week, first week = 1
    Returns:
        week_data: Loads a week from file, if file does not exists creates empty week
    """
    file_path = get_file_path(year, week_number)
    
    if (file_helper.file_exists(file_path)):
        week_data = file_helper.load_json(file_path)
    else:
        week_data = create_new_week(year, week_number)

    week_data = add_days_name_to_date(week_data)
    return week_data

def create_new_week(year, week_number):
    """Summary Creates an empty week for the specified week
    Args:
        year (int): Year of weeknumber
        week_number (int):  Corrected number of week, first week = 1
    Returns:
        week_data: Returns a new week data structure
    """
    week_data = {
        'new_week': True,
        'week_number': week_number,
        'year': year,
        'days': []
    }

    dates = date_helper.calculate_dates_of_week(year, week_number)
    
    id = 1
    for date in dates: # set the dates in the dict weekday
        week_data['days'].append({
            'id': "day" + str(id),
            'date': date,
        })
        id += 1

    return week_data

def update_week(request, year, week_number):
    """Summary Updates the week with the data from the form
    Args:
        request (Request): Form from the UI
        year (int): Year of weeknumber
        week_number (int):  Corrected number of week, first week = 1
    Returns:
        week_data: Returns the updated week data structure
    """
    week_data = load_week(year, week_number) 
    
    form_request = request.form.to_dict() # create a dict from the form
    day_name = list(form_request)[0].split('_') # get the day from the first name
    day = next((x for x in week_data['days'] if x.get('id') == day_name[0]), None)

    for key, value in form_request.items(): # auto update the data
        key = key.split('_')[1]
        day[key] = value

    file_name = file_helper.upload_image(request) # save the image
    if file_name:
        day['image'] = file_name
    week_data['new_week'] = False 

    data_path = get_file_path(year, week_number) 
    file_helper.save_json(data_path, week_data) # save the file

    return week_data

def get_file_path(year, week_number):
    """Summary returns the file name for the file of a week
    Args:
        data_path (String): Folder where data is stored
        year (String): Year of weeknumber
        week_number (String):  Corrected number of week, first week = 1
    Returns:
        String: Returns the file path to a week file
    """
    return '%s%s%s%s%s%s' % (config.DATA_PATH, '/week_data/' , year, '_', week_number, '.txt')


def add_days_name_to_date(week_data):
    """add the name of the day to the data
    Args:
        week_data (dict): week_data
    Returns:
        String: Returns the week_data with added names
    """
    counter = 0
    if (week_data.get('days')):
        for day in week_data['days']:
            day['day_name'] = config.WEEKDAYS_NAME[counter]
            counter += 1
    return week_data