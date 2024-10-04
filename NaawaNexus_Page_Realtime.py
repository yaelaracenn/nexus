import streamlit as st
import pandas as pd
from dateutil import parser
import NaawaNexus_LinearRegression
import statsmodels.api as sm
import plotly.express as px
import time
import FakeRealTimeGenerator2 as TimeGenerator

supported_file_extensions_list = ['csv', 'xls', 'xlsx']
dependent_variable_str = 'Leads'
independent_variables_list = ['RADIO_GRP20', 'PRENSA_GRP', 'TV_GRPA20_40', 'Celebrity', 'Ssanta', 'Reyes', 'Navidad', 'PteOct', 'PteDic', 'Abr', 'May', 'Sep', 'Oct', 'Nov', 'verano', 'SegundaSemanaMes', 'UltimaSemanaMes']


def Page_RealTime():

    model_file = st.file_uploader('Upload Model')
    model = load_pickle(model_file)

    input_data_file = st.file_uploader('Database File uploader')

    if input_data_file is not None:

        # Extract File Name and File Extension
        file_name_str = input_data_file.name
        file_extension_str = file_name_str[file_name_str.find('.') + 1:]
        
        # Check if File Extension is correct.
        # If file extension is not correct show an error
        if file_extension_str not in supported_file_extensions_list:
            extension_error_body_str = "File Extension '" + file_extension_str + "' is not correct. Must be one of these: csv, xls, xlsx."
            st.error(body = extension_error_body_str)
        
        # If file extension is correct start modelling
        else:
            # First, the data must be read
            if file_extension_str == 'csv':
                data_df = pd.read_csv(input_data_file)
            elif (file_extension_str == 'xls') or (file_extension_str == 'xlsx'):
                data_df = pd.read_excel(input_data_file)
            columns_list = data_df.columns.to_list()

    time_variable_popover = st.popover('Seleccione Variable Temporal')
    time_variable_str = time_variable_popover.radio(label = 'Seleccione Variable Temporal', options = columns_list, index = None)

    real_time_checkbox = st.checkbox('Real Time')

    while real_time_checkbox:
        # Sleep 5 seconds
        time.sleep(5)

        data_df = TimeGenerator.add_new_row(data_df = data_df, time_variable_str = time_variable_str, time_delta = 7)
        
        modelVsReal = NaawaNexus_LinearRegression.generateActualVsModel(data_df = data_df, model = model, dependent_variable_str = dependent_variable_str, independent_variables_list = independent_variables_list, time_variable_str = time_variable_str)

        condition = (modelVsReal['Type'].isin(['Model', 'Actual']))
        df_modelVSactual = modelVsReal[condition]
        print(model.summary())

        # Generate Model vs Actual line graph
        lineChart = px.line(data_frame = df_modelVSactual, x = 'semana', y = 'Leads', title = 'Model Vs Actual Chart', labels = 'Type', line_group='Type', color = 'Type', color_discrete_sequence = ['red', 'blue'])

        with st.container(border = True):
            st.plotly_chart(figure_or_data = lineChart, use_container_width = True)

    
