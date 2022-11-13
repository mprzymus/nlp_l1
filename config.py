import pandas as pd

START = "2019-09-01"
END = "2022-11-12"


def date_range():
    dates = [d.to_pydatetime().date() for d in pd.date_range(START, END).to_list()]
    dates.reverse()
    return dates
