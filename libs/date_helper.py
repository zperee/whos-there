import datetime
import time

def validate_week_input(year, week_number):
    """Summary
    Args:
        year (String): Year of weeknumber
        week_number (String):  Corrected number of week, first week = 1
    Returns:
        boolean: Returns if the data input is valid
    """
    valid = False
    if ((week_number and week_number.isdigit()) and (int(week_number) >= 0 and int(week_number) <= 52)):
        if ((year and year.isdigit()) and (int(year) >= 1970 and int(year) <= 2100)):
            valid = True

    return valid

def get_current_week_number():
    """Summary
    Returns:
        int: Gets the current week number
    """
    week_number = datetime.date.today().isocalendar()[1]
    return week_number

def get_current_year():
    """Summary
    Returns:
        int: Gets the current year
    """  
    now = datetime.datetime.now()
    return now.year

def get_week_number_url(**weeks_from_now):
    """Summary
    Args:
        weeks_from_now (int): Weeks in the future
    Returns:
        week_number: Week number in the future
    """
    year = get_current_year()
    week_number = get_current_week_number()
    
    if weeks_from_now:
        week_number += weeks_from_now
        if week_number > 52:
            week_number = week_number - 52
            year += 1
        
    return year

def calculate_week_from_date(date):
    """Summary
    Args:
        date (): Date
    Returns:
        week_number: Week number of the date
    """
    week = date.isocalendar()[:2]
    return week

def calculate_dates_of_week(year, week_number):
    """Summary
    Args:
        year (int): Year of weeknumber
        week_number (int): Corrected number of week, first week = 1
    Returns:
        List: A list of all dates that are in a entered week
    """
    first_date = _calculate_first_date_of_week(year, week_number)
    all_dates_of_week = _calculate_all_dates_of_week(first_date)
    return all_dates_of_week

# Private definitions
def _calculate_first_date_of_week(year, week_number):
    if(validate_week_input(year, week_number)):
        year = int(year)
        week_number = int(week_number)
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