from . import data_helper
from . import week_date_helper
from . import config

def load_week(year, week_number):
    """Summary
    Args:
        data_path (String): Folder where data is stored
        year (String): 
        week_number (String):  Corrected number of week, first week = 1
    Returns:
        week_data: Loads a week from file, if file does not exists creates empty week
    """
    file_path = get_file_path(year, week_number)
    
    if (data_helper.file_exists(file_path)):
        week_data = data_helper.load_json(file_path)
    else:
        week_data = create_new_week(year, week_number)

    return week_data

def create_new_week(year, week_number):
    """Summary
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

    dates = week_date_helper.calculate_dates_of_week(year, week_number)
    id = 1
    # ToDo load attending dynamic from config
    for date in dates:
        week_data['days'].append({
            'id': "day" + str(id),
            'date': date,
            'menu': '',
            'image': '',
            'time': '',
            'attending': {
                'patrick': None,
                'silvia': None,
                'giulia': None,
                'amelia': None,
                'elia': None,
            }
        })
        id += 1
    return week_data

def update_week(request, year, week_number):
    """Summary
    Args:
        data_path (String): Folder where data is stored
        request_form (): Form from the UI
        year (int): Year of weeknumber
        week_number (int):  Corrected number of week, first week = 1
    Returns:
        week_data: Returns the updated week data structure
    """
    week_data = load_week(year, week_number)
    print(request.form)
    form_request = request.form.to_dict()
    day_name = list(form_request)[0].split('_')
    day = next((x for x in week_data['days'] if x.get('id') == day_name[0]), None)

    for key, value in form_request.items():
        key = key.split('_')[1]
        day[key] = value

    file_name = data_helper.upload_image(request)
    day['image'] = file_name
    week_data['new_week'] = False

    data_path = get_file_path(year, week_number)
    data_helper.save_json(data_path, week_data)

    return week_data

def get_file_path(year, week_number):
    """Summary
    Args:
        data_path (String): Folder where data is stored
        year (String): Year of weeknumber
        week_number (String):  Corrected number of week, first week = 1
    Returns:
        String: Returns the file path to a week file
    """
    return '%s%s%s%s%s%s' % (config.DATA_PATH, '/' , year, '_', week_number, '.txt')
