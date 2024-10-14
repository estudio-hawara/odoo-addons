from datetime import date, timedelta
from math import ceil

def get_sequential_dates_value(record, batch_info):
    if not record.value_type == 'sequential_dates':
        raise Exception('A random record cannot be created for this {} field'.format(record.value_type))

    return get_sequential_dates(
        date_min=record.sequential_dates_min,
        date_max=record.sequential_dates_max,
        row_count=batch_info.row_count,
        row_number=batch_info.row_number)

def get_sequential_dates(date_min=None, date_max=None, row_count=1, row_number=1):
    if not date_max:
        date_max = date.today()
    if not date_min:
        date_min = date(date_max.year, 1, 1)
    period = date_max - date_min
    rows_per_day = row_count / (period.days + 1)
    if row_number > row_count:
        row_number = row_count
    corresponding_day = ceil((row_number - 1) / rows_per_day)
    return date_min + timedelta(days=corresponding_day)