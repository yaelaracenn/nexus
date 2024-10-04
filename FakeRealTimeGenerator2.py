import pandas as pd
import numpy as np
import pages.Important_Dates as ImportantDates
import pages.NaawaNexus_Functions_Time as NNFT

def add_new_row(data_df, time_variable_str, time_delta):

    new_data_df = pd.read_excel('Modelling Hair Beauty BBDD 2023 - Live Data.xls')
# time_variable_str = 'semana'
# time_delta = 7

    last_row_date = data_df.iloc[-1][time_variable_str]

    next_date = last_row_date + pd.Timedelta(days = time_delta)
    
    new_row_df = new_data_df[new_data_df[time_variable_str] == next_date]

    data_df = pd.concat([data_df, new_row_df], ignore_index = True)

    return data_df