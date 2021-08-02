import pandas as pd


def object_datetime(column):
    return pd.to_datetime(column)


def datetime_julian(column):
    date_col = object_datetime(column)
    return pd.DatetimeIndex(date_col).to_julian_date()


