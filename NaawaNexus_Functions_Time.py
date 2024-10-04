import calendar
from datetime import timedelta, datetime
from pages.Important_Dates import spain_holidays, spain_special_days, season_start_days

christmas_day = 25
christmas_month = 12
reyes_day = 6
reyes_month = 1

def calculate_easter_sunday(year):
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return year, month, day

def calculate_semana_santa(year):
    # Semana Santa is the week leading up to Easter Sunday
    easter_date = calculate_easter_sunday(year)
    easter_sunday = calendar.datetime.date(year, easter_date[1], easter_date[2])
    semana_santa_start = easter_sunday - timedelta(days=7)
    semana_santa_end = easter_sunday
    return semana_santa_start, semana_santa_end

def is_semana_santa_week(date_string, date_format):
    date = datetime.strptime(date_string,date_format)
    year = date.year
    semana_santa_start, semana_santa_end = calculate_semana_santa(year)
    if (date.date() > semana_santa_start) and (date.date() <= semana_santa_end):
        is_semana_santa = 1
    else:
        is_semana_santa = 0
    return is_semana_santa

def calculate_week(date, first_weekday):
    # date = datetime.strptime(date, date_format).date()
    weekday = date.weekday()
    week_start = date - timedelta(days = weekday)
    week_end = date + timedelta(days = 6 - weekday)

    if first_weekday == 'Tuesday':
        week_start = week_start + timedelta(days = 1)
        week_end = week_end + timedelta(days = 1)
    elif first_weekday == 'Wednesday':
        week_start = week_start + timedelta(days = 2)
        week_end = week_end + timedelta(days = 2)
    elif first_weekday == 'Thursday':
        week_start = week_start + timedelta(days = 3)
        week_end = week_end + timedelta(days = 3)
    elif first_weekday == 'Friday':
        week_start = week_start + timedelta(days = 4)
        week_end = week_end + timedelta(days = 4)
    elif first_weekday == 'Saturday':
        week_start = week_start + timedelta(days = 5)
        week_end = week_end + timedelta(days = 5)
    elif first_weekday == 'Sunday':
        week_start = week_start + timedelta(days = 6)
        week_end = week_end + timedelta(days = 6)

    return week_start, week_end

def is_any_holiday_week(date_string, date_format, first_week_day):
    ## Funtion to see if a date is in a week with any holiday
    # For example: Christmas week is the week containing Christmas Day

    date = datetime.strptime(date_string,date_format)
    week_start, week_end = calculate_week(date, first_week_day)

    year = date.year
    # Christmas:
    holiday_date_start = spain_holidays['NAVIDAD']
    holiday_date = datetime(year, int(holiday_date_start[3:]), int(holiday_date_start[0:2])).date()
    if (holiday_date >= week_start.date()) and (holiday_date <= week_end.date()):
        is_christmas = 1
    else:
        is_christmas = 0
    
    # Reyes
    holiday_date_start = spain_holidays['REYES']
    holiday_date = datetime(year, int(holiday_date_start[3:]), int(holiday_date_start[0:2])).date()
    if (holiday_date >= week_start.date()) and (holiday_date <= week_end.date()):
        is_reyes = 1
    else:
        is_reyes = 0

    # Fin de Año
    holiday_date_start = spain_holidays['FIN ANNO']
    holiday_date = datetime(year, int(holiday_date_start[3:]), int(holiday_date_start[0:2])).date()
    if (holiday_date >= week_start.date()) and (holiday_date <= week_end.date()):
        is_fin_anno = 1
    else:
        is_fin_anno = 0

    # Puente de Mayo
    holiday_date_start = spain_holidays['PTE MAYO']
    holiday_date = datetime(year, int(holiday_date_start[3:]), int(holiday_date_start[0:2])).date()
    if (holiday_date >= week_start.date()) and (holiday_date <= week_end.date()):
        is_pte_mayo = 1
    else:
        is_pte_mayo = 0

    # Puente de Mayo
    holiday_date_start = spain_holidays['PTE MAYO']
    holiday_date = datetime(year, int(holiday_date_start[3:]), int(holiday_date_start[0:2])).date()
    if (holiday_date >= week_start.date()) and (holiday_date <= week_end.date()):
        is_pte_mayo = 1
    else:
        is_pte_mayo = 0

    # Puente de Agosto
    holiday_date_start = spain_holidays['PTE AGOSTO']
    holiday_date = datetime(year, int(holiday_date_start[3:]), int(holiday_date_start[0:2])).date()
    if (holiday_date >= week_start.date()) and (holiday_date <= week_end.date()):
        is_pte_agosto = 1
    else:
        is_pte_agosto = 0

    # Puente de Septiembre
    holiday_date_start = spain_holidays['PTE SEPTIEMBRE']
    holiday_date = datetime(year, int(holiday_date_start[3:]), int(holiday_date_start[0:2])).date()
    if (holiday_date >= week_start.date()) and (holiday_date <= week_end.date()):
        is_pte_septiembre = 1
    else:
        is_pte_septiembre = 0

    # Puente de Octubre
    holiday_date_start = spain_holidays['PTE OCTUBRE']
    holiday_date = datetime(year, int(holiday_date_start[3:]), int(holiday_date_start[0:2])).date()
    if (holiday_date >= week_start.date()) and (holiday_date <= week_end.date()):
        is_pte_octubre = 1
    else:
        is_pte_octubre = 0

    # Puente de Noviembre
    holiday_date_start = spain_holidays['PTE NOVIEMBRE']
    holiday_date = datetime(year, int(holiday_date_start[3:]), int(holiday_date_start[0:2])).date()
    if (holiday_date >= week_start.date()) and (holiday_date <= week_end.date()):
        is_pte_noviembre = 1
    else:
        is_pte_noviembre = 0

    # Puente de Diciembre
    holiday_date_start = spain_holidays['PTE DICIEMBRE']
    holiday_date = datetime(year, int(holiday_date_start[3:]), int(holiday_date_start[0:2])).date()
    if (holiday_date >= week_start.date()) and (holiday_date <= week_end.date()):
        is_pte_diciembre = 1
    else:
        is_pte_diciembre = 0

    # Semana Santa
    is_semana_santa = is_semana_santa_week(date_string = date_string, date_format = date_format)

    is_any_holiday_week = {
        'NAVIDAD'       : is_christmas,
        'REYES'         : is_reyes,
        'FIN ANNO'      : is_fin_anno,
        'PTE MAYO'      : is_pte_mayo,
        'PTE AGOSTO'    : is_pte_agosto,
        'PTE SEPTIEMBRE': is_pte_septiembre,
        'PTE OCTUBRE'   : is_pte_octubre,
        'PTE NOVIEMBRE' : is_pte_noviembre,
        'PTE DICIEMBRE' : is_pte_diciembre,
        'SEMANA SANTA'  : is_semana_santa
    }

    return is_any_holiday_week

def is_season(date_string, date_format, first_week_day):
    date = datetime.strptime(date_string,date_format)
    week_start, week_end = calculate_week(date, first_week_day)

    year = date.year

    # Spring
    season_start = season_start_days['SPRING']
    season_end = season_start_days['SUMMER']

    season_start_date = datetime(year, int(season_start[3:]), int(season_start[0:2])).date()
    season_end_date = datetime(year, int(season_end[3:]), int(season_end[0:2])).date()

    if (season_start_date >= week_start.date()) and (season_start_date <= week_end.date()):
        is_spring = 1
    elif (season_end_date >= week_start.date()) and (season_end_date <= week_end.date()):
        is_spring = 0
    elif (date.date() >= season_start_date) and (date.date() < season_end_date):
        is_spring = 1
    else:
        is_spring = 0

    # Summer
    season_start = season_start_days['SUMMER']
    season_end = season_start_days['AUTUMN']

    season_start_date = datetime(year, int(season_start[3:]), int(season_start[0:2])).date()
    season_end_date = datetime(year, int(season_end[3:]), int(season_end[0:2])).date()

    if (season_start_date >= week_start.date()) and (season_start_date <= week_end.date()):
        is_summer = 1
    elif (season_end_date >= week_start.date()) and (season_end_date <= week_end.date()):
        is_summer = 0
    elif (date.date() >= season_start_date) and (date.date() < season_end_date):
        is_summer = 1
    else:
        is_summer = 0

    # Autumn
    season_start = season_start_days['AUTUMN']
    season_end = season_start_days['WINTER']

    season_start_date = datetime(year, int(season_start[3:]), int(season_start[0:2])).date()
    season_end_date = datetime(year, int(season_end[3:]), int(season_end[0:2])).date()

    if (season_start_date >= week_start.date()) and (season_start_date <= week_end.date()):
        is_autumn = 1
    elif (season_end_date >= week_start.date()) and (season_end_date <= week_end.date()):
        is_autumn = 0
    elif (date.date() >= season_start_date) and (date.date() < season_end_date):
        is_autumn = 1
    else:
        is_autumn = 0

    # Winter
    season_start = season_start_days['WINTER']
    season_end = season_start_days['SPRING']

    if date.month >= 11:
        season_start_date = datetime(year, int(season_start[3:]), int(season_start[0:2])).date()
        season_end_date = datetime(year + 1, int(season_end[3:]), int(season_end[0:2])).date()
    else:
        season_start_date = datetime(year - 1, int(season_start[3:]), int(season_start[0:2])).date()
        season_end_date = datetime(year, int(season_end[3:]), int(season_end[0:2])).date()

    if (season_start_date >= week_start.date()) and (season_start_date <= week_end.date()):
        is_winter = 1
    elif (season_end_date >= week_start.date()) and (season_end_date <= week_end.date()):
        is_winter = 0
    elif (date.date() >= season_start_date) and (date.date() < season_end_date):
        is_winter = 1
    else:
        is_winter = 0

    is_season = {
        'SPRING'    : is_spring,
        'SUMMER'    : is_summer,
        'AUTUMN'    : is_autumn,
        'WINTER'    : is_winter
    }

    return is_season

def is_special_date_week(date_string, date_format, first_week_day):

    date = datetime.strptime(date_string,date_format)
    week_start, week_end = calculate_week(date, first_week_day)

    year = date.year
    # San Valentin:
    special_date_start = spain_special_days['SAN VALENTIN']
    special_date = datetime(year, int(special_date_start[3:]), int(special_date_start[0:2])).date()
    if (special_date >= week_start.date()) and (special_date <= week_end.date()):
        is_san_valentin = 1
    else:
        is_san_valentin = 0

    is_special_date = {
        'SAN VALENTIN'      : is_san_valentin
    }

    return is_special_date

def is_month_week(date_string, date_format, first_week_day):

    is_january = 0
    is_february = 0
    is_march = 0
    is_april = 0
    is_may = 0
    is_june = 0
    is_july = 0
    is_august = 0
    is_september = 0
    is_october = 0
    is_november = 0
    is_december = 0

    date = datetime.strptime(date_string,date_format)
    week_start, week_end = calculate_week(date, first_week_day)

    year = date.year

    if week_start.date().month != week_end.date().month:
        
        aux_date = week_start.date()
        month_to_check = aux_date.month
        month_1_count = 0
        month_2_count = 0

        while aux_date <= week_end.date():
            if aux_date.month == month_to_check:
                month_1_count += 1
                aux_date = aux_date + timedelta(days=1)
            else:
                month_2_count += 1
                aux_date = aux_date + timedelta(days=1)
        
        if month_1_count > month_2_count:
            month = week_start.date().month
        else:
            month = week_end.date().month

    else:
        month = week_start.date().month

    if month == 1:
        is_january = 1
    elif month == 2:
        is_february = 1
    elif month == 3:
        is_march = 1
    elif month == 4:
        is_april = 1
    elif month == 5:
        is_may = 1
    elif month == 6:
        is_june = 1
    elif month == 7:
        is_july = 1
    elif month == 8:
        is_august = 1
    elif month == 9:
        is_september = 1
    elif month == 10:
        is_october = 1
    elif month == 11:
        is_november = 1
    elif month == 12:
        is_december = 1

    is_month = {
        'JANUARY'   : is_january,
        'FEBRUARY'  : is_february,
        'MARCH'     : is_march,
        'APRIL'     : is_april,
        'MAY'       : is_may,
        'JUNE'      : is_june,
        'JULY'      : is_july,
        'AUGUST'    : is_august,
        'SEPTEMBER' : is_september,
        'OCTOBER'   : is_october,
        'NOVEMBER'  : is_november,
        'DECEMBER'  : is_december
    }

    return is_month

def is_week_number(date_string, date_format, first_week_day):
    
    is_first_week = 0
    is_second_week = 0
    is_third_week = 0
    is_fourth_week = 0
    is_last_week = 0

    date = datetime.strptime(date_string,date_format)
    week_start, week_end = calculate_week(date, first_week_day)

    week_start_day = week_start.date().day
    week_start_month = week_start.date().month

    if (week_start_day >= 1) and (week_start_day < 5):
        is_first_week = 1
    elif (week_start_day >= 5) and (week_start_day < 12):
        is_second_week = 1
    elif (week_start_day >= 12) and (week_start_day < 19):
        is_third_week = 1
    elif (week_start_day >= 19) and (week_start_day < 26):
        is_fourth_week = 1
    elif (week_start_day == 26):
        is_last_week = 1
    elif (week_start_day == 27) and (week_start_month == 2):
        is_first_week = 1
    elif (week_start_day == 27) and (week_start_month != 2):
        is_last_week = 1
    elif (week_start_day == 28) and (week_start_month in [1, 3, 5, 7, 8, 10, 12]):
        is_last_week = 1
    elif (week_start_day == 28) and (week_start_month in [2, 4, 6, 9, 11]):
        is_first_week = 1
    elif (week_start_day >= 29):
        is_first_week = 1

    is_week = {
        'FIRST' : is_first_week,
        'SECOND': is_second_week,
        'THIRD' : is_third_week,
        'FOURTH': is_fourth_week,
        'LAST'  : is_last_week
    }

    return is_week

def is_month_start_or_end(date_string, date_format, first_week_day):
    
    is_month_start = 0
    is_month_end = 0

    date = datetime.strptime(date_string,date_format)
    week_start, week_end = calculate_week(date, first_week_day)

    month = date.month
    year = date.year

    month_start_day = datetime(year, month, 1).date()
    month_end_day = datetime(year, month, 15).date()
    
    if (month_start_day >= week_start.date()) and (month_start_day <= week_end.date()):
        is_month_start = 1
    elif month_end_day > week_end.date():
        is_month_start = 1
    else:
        is_month_end = 1

    is_month_start_or_end = {
        'START' : is_month_start,
        'END'   : is_month_end
    }

    return is_month_start_or_end

def is_month_change(date_string, date_format, first_week_day):
    
    is_month_change = 0

    date = datetime.strptime(date_string,date_format)
    week_start, week_end = calculate_week(date, first_week_day)

    month = date.month
    year = date.year

    if month < 12:
        next_month_start_day = datetime(year, month + 1, 1).date()
    else:
        next_month_start_day = datetime(year + 1, 1, 1).date()

    month_end_day = next_month_start_day - timedelta(days = 1)

    if (month_end_day >= week_start.date()) and (month_end_day <= week_end.date()):
        is_month_change = 1

    return is_month_change

def is_holiday(date_string, date_format, first_week_day):
    
    is_holiday = 0

    date = datetime.strptime(date_string,date_format)
    week_start, week_end = calculate_week(date, first_week_day)

    is_any_holiday = is_any_holiday_week(date_string, date_format, first_week_day)

    for key, value in is_any_holiday.items():
        if value == 1:
            is_holiday = 1
        else:
            pass

    return is_holiday

def find_date_format(date_str):
    # Define a list of possible date formats
    possible_formats = ["%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d", "%d-%m-%Y", "%m-%d-%Y", "%Y-%m-%d"]
    
    for date_format in possible_formats:
        try:
            # If parsing succeeds, return the format
            datetime.strptime(date_str, date_format)
            return date_format
        except ValueError:
            # If parsing fails, try the next format
            continue
    
    # Return None if no format matched
    return None