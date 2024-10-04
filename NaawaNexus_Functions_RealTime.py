import streamlit as st
from datetime import datetime
import pandas as pd
import plotly.express as px
from NaawaNexus_Menu import menu_with_redirect

from streamlit_autorefresh import st_autorefresh

import time
import FakeRealTimeGenerator2 as TimeGenerator
import pages.NaawaNexus_Functions_LinearRegression as NaawaNexus_Functions_LinearRegression

# To parametrize
supported_file_extensions_list = ['csv', 'xls', 'xlsx']

def Page_RealTime(languaje):
    # st.success('Real Time')
    
    input_data_file = st.session_state.input_data_file
    independent_variables_list = st.session_state.independent_variables_list
    time_variable_str = st.session_state.time_variable_str
    model = st.session_state.model
    dependent_variable_str = st.session_state.dependent_variable_str
   
    real_time_data_df = pd.read_excel(input_data_file, sheet_name = 'BBDD')

    real_time_checkbox = st.checkbox('Real Time')
    count = 1

    if real_time_checkbox:     
        
        if 'real_time_data_df' not in st.session_state:
            st.session_state.real_time_data_df = real_time_data_df

        st.session_state.real_time_data_df = TimeGenerator.add_new_row(data_df = st.session_state.real_time_data_df, time_variable_str = time_variable_str, time_delta = 7)
        
        st.session_state.modelVsReal = NaawaNexus_Functions_LinearRegression.generateActualVsModel(data_df = st.session_state.real_time_data_df, model = model, dependent_variable_str = dependent_variable_str, independent_variables_list = independent_variables_list, time_variable_str = time_variable_str)

        condition = (st.session_state.modelVsReal['Type'].isin(['Model', 'Actual']))
        st.session_state.df_modelVSactual = st.session_state.modelVsReal[condition]

        # Generate Model vs Actual line graph
        st.session_state.lineChart = px.line(data_frame = st.session_state.df_modelVSactual, x = time_variable_str, y = dependent_variable_str, title = 'Model Vs Actual Chart', labels = 'Type', line_group='Type', color = 'Type', color_discrete_sequence = ['red', 'blue'])
        
        with st.container(border = True):
            st.plotly_chart(figure_or_data = st.session_state.lineChart, use_container_width = True)
                
        st_autorefresh(interval = 1 * 1000, key = "main_Refresh_" + str(count), debounce = False)
        count += 1
        # time.sleep(5)
        # st_autorefresh()