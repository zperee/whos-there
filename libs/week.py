import datetime
import time

def get_week(weeks_from_current=0):
    """Summary
    Args:
        weeks_from_current (int): Get which week form current 0 = current
    Returns:
        dict: {"week_number": int, "dates": {"Monday": date_string}}
    """
    current_week = get_current_week_number()
    current_week = current_week + weeks_from_current
    dates = calculate_dates_of_week(current_week)
    
    weekDays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
    zipObj = zip(weekDays, dates)
    weekDict = dict(zipObj)

    return {"week_number": current_week, "dates": weekDict}

def get_current_week_number():
    """Summary
    Returns:
        int: Gets the current week number
    """
    week_number = datetime.date.today().isocalendar()[1]
    return week_number

def calculate_dates_of_week(week_number, year = 0):
    """Summary
    Args:
        week_number (int): Not corrected number of week, first week = 0
        year (int): Year of weeknumber - default current year
    Returns:
        List: A list of all dates that are in a entered week
    """
    if (year == 0):
        now = datetime.datetime.now()
        year = now.year
        
    if (week_number >= 0):
        first_date = _calculate_first_date_of_week(week_number, year)
        return _calculate_all_dates_of_week(first_date)

# Private definitions
def _calculate_first_date_of_week(week_number, year):
    week_string = '%s-W%s' % (year,week_number - 1) #Counting of weeks starts with 0
    first_day = time.asctime(time.strptime(week_string + '-1', "%Y-W%W-%w")) # -1 = Monday
    return first_day

def _calculate_all_dates_of_week(start_date):
    start_date = datetime.datetime.strptime(start_date, '%a %b %d %H:%M:%S %Y') 
    dates = [start_date.strftime('%d.%m.%Y')] 
    for i in range(1, 7): 
        day = start_date + datetime.timedelta(days=i)
        dates.append(day.strftime('%d.%m.%Y'))

    return dates 

def __private():
    return "1"

print(get_week())
