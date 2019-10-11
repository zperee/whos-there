from . import data_helper
from . import week_date_helper

def load_week(data_path, year, week_number):
    file_path = get_file_name(data_path, year, week_number)
    
    if (data_helper.file_exists(file_path)):
        week_data = data_helper.load_json(file_path)
    else:
        week_data = create_new_week(year, week_number)

    return week_data

def create_new_week(year, week_number):
    week_data = {
        'week_number': week_number,
        'year': year,
        'days': []
    }

    dates = week_date_helper.calculate_dates_of_week(year, week_number)
    id = 0
    # ToDo load attending dynamic from config
    for date in dates:
        week_data['days'].append({
            'id': "day" + str(id),
            'date': date,
            'menu': '',
            'image': '',
            'time': '',
            'attending': {
                'elia': False,
                'amelia': False,
                'giulia': False,
                'silvia': False,
                'patrick': False,
            }
        })
        id += 1
    return week_data

def update_week(data_path, request_form, year, week_number):
    file_path = get_file_name(data_path, year, week_number)
    week_data = load_week(data_path, year, week_number)

    form_request = request_form.to_dict()
    day_name = list(form_request)[0].split('_')
    day = next((x for x in week_data['days'] if x.get('id') == day_name[0]), None)

    for key, value in form_request.items():
        key = key.split('_')[1]
        day[key] = value

    print(week_data)
    data_helper.save_json(file_path, week_data)

    return week_data

def get_file_name(data_path, year, week_number):
    return '%s%s%s%s%s' % (data_path, year, '_', week_number, '.txt')
