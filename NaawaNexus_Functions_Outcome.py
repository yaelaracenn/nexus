import streamlit as st
from datetime import datetime
import pandas as pd
import plotly.express as px

# To parametrize
supported_file_extensions_list = ['csv', 'xls', 'xlsx']

def Page_Outcome(languaje):
    if 'clicked' not in st.session_state:
        st.session_state.clicked = False
    
    ## Outcome Page function
    # Title and Header
    if languaje == 'ENG':
        st.title(body = 'Outcome')
        st.subheader(body = 'Analyze attribution and the ROI of your efforts.')
    elif languaje == 'SPA':
        st.title(body = 'Outcome')
        st.subheader(body = 'Analyze attribution and the ROI of your efforts.')

    time_variable_str = st.session_state.time_variable_str
    input_data_file = st.session_state.input_data_file

    file_name_str = input_data_file.name
    file_extension_str = file_name_str[file_name_str.find('.') + 1:]

    # try:
        # First, the data must be read
    if file_extension_str == 'csv':
        investment_data_df = pd.read_csv(input_data_file)
    elif (file_extension_str == 'xls') or (file_extension_str == 'xlsx'):
        investment_data_df = pd.read_excel(input_data_file, sheet_name = 'Investment')

        ###### SOLUCION TEMPORAL #####
        revenue_data = pd.read_excel(input_data_file, sheet_name = 'Revenue')

    # Date Input
    # Find min and max date in the original data to limit the date input
    # Get all dates
    dfDates = investment_data_df
    dfDates[time_variable_str] = pd.to_datetime(dfDates[time_variable_str])
    # Find min date
    min_date = str(dfDates[time_variable_str].min())
    min_date = min_date[:min_date.find(' ')]
    # Find max date
    max_date = str(dfDates[time_variable_str].max())
    max_date = max_date[:max_date.find(' ')]

    # Date filter form.
    # Show a form to select the date range
    with st.form(key = 'Date Filter Form'):
    # with st.container():
        fromDate = st.date_input(label = 'From:', format='YYYY-MM-DD', value = datetime.strptime(min_date, '%Y-%m-%d'))
        toDate = st.date_input(label = 'To:', format = 'YYYY-MM-DD', value = datetime.strptime(max_date, '%Y-%m-%d'))

        st.form_submit_button(label = 'Apply Date Filter')

        # Generate dataframe with Invesment and Revenue data for each variable to study
        # This DataFrame will contain the Total Investment and Revenue for each variable, and it's percentages.
        # Set filter condition with the desired dates
        condition = (investment_data_df[time_variable_str] >= str(fromDate)) & (investment_data_df[time_variable_str] <= str(toDate))

        # Filter investment and revenue data with the condition
        investments = investment_data_df[condition]
        revenues = revenue_data[condition]

        # Generate the DataFrame that will be used to plot the information
        columnsRevVsInv = ['Variable', 'Investment', 'Revenue', 'Investment Percentage', 'Revenue Percentage', 'Investment Percentage Text', 'Revenue Percentage Text', 'Return Index', 'Group']
        dfRevVsInv = pd.DataFrame(columns = columnsRevVsInv)

        # Get all the variable names to study
        headers = investments.columns.to_list()
        # Delete the dates header name
        headers.remove(time_variable_str)

        # Initiate the Investment and Revenues totals
        totalInvestment = 0
        totalRevenue = 0

        # Loop all the headers to calulate the sums of all the variables
        for header in headers:
            # Generate the new row that will be added to the DataFrame
            new_row = {
                # Variable name
                columnsRevVsInv[0] : header,
                # Investments sum
                columnsRevVsInv[1] : investments[header].sum(),
                # Revenues sum
                columnsRevVsInv[2] : revenues[header].sum(),
                columnsRevVsInv[8] : 'Group'
                }
            # Add sums to totals
            # print(new_row)
            totalInvestment += investments[header].sum()
            totalRevenue += revenues[header].sum()
            # Add row to DataFrame
            dfRevVsInv.loc[len(dfRevVsInv)] = new_row

        # Calculate the percentages columns
        dfRevVsInv[columnsRevVsInv[3]] = round((dfRevVsInv[columnsRevVsInv[1]] / totalInvestment) * 100, 1)
        dfRevVsInv[columnsRevVsInv[4]] = round((dfRevVsInv[columnsRevVsInv[2]] / totalRevenue) * 100, 1)
        # Generate the columns that will give names to the values in the graph
        dfRevVsInv[columnsRevVsInv[5]] = dfRevVsInv[columnsRevVsInv[3]].astype(str) + ' %'
        dfRevVsInv[columnsRevVsInv[6]] = dfRevVsInv[columnsRevVsInv[4]].astype(str) + ' %'
        dfRevVsInv[columnsRevVsInv[7]] = round(dfRevVsInv[columnsRevVsInv[2]] /dfRevVsInv[columnsRevVsInv[1]],2)

        # Data will be shown in 2 columns
        filtCol1, filtCol2 = st.columns(2)
        
        # Generate column 1 with Investment and Revenues percentages
        with filtCol1:
            invCol, revCol = st.columns(2)
            
            with invCol.container(border = True):
                invBarChart = px.bar(data_frame = dfRevVsInv, x = 'Group', y = 'Investment Percentage', color = 'Variable', title = 'Investment', text = 'Investment Percentage Text')
                st.plotly_chart(figure_or_data = invBarChart, use_container_width = True)

            with revCol.container(border = True):

                revBarChart = px.bar(data_frame = dfRevVsInv, x = 'Group', y = 'Revenue Percentage', color = 'Variable', title = 'Revenue', text = 'Revenue Percentage Text')
                st.plotly_chart(figure_or_data = revBarChart, use_container_width = True)

        with filtCol2.container(border = True):

            retBarChart = px.bar(data_frame = dfRevVsInv, x = 'Return Index', y = 'Variable', orientation = 'h', color = 'Variable', title = 'Return Index', text = 'Return Index')
            retBarChart.add_vline(x=1, line_width=1, line_dash="dash", line_color="black")

            st.plotly_chart(figure_or_data = retBarChart, use_container_width = True)

    # except:
        # if languaje == 'ENG':
        #     st.error('Make sure a sheet with the data exists and it is named "Investment"')
        # elif languaje == 'SPA':
        #     st.error('Asegurate que existe una hoja con datos llamada "Investment"')



def update_outcome (fromDate, toDate, investment_data_df, revenue_data, time_variable_str):
    st.session_state.clicked = True        
    


    
    