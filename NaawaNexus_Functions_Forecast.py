import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import os
import statsmodels.api as sm
import plotly.graph_objects as go

def Page_Forecast(languaje):

    input_data_file = st.session_state.input_data_file
    modelVsReal = st.session_state.modelVsReal
    model = st.session_state.model
    time_variable_str = st.session_state.time_variable_str
    independent_variables_list = st.session_state.independent_variables_list
    dependent_variable_str = st.session_state.dependent_variable_str
    # Path to Forecast Scenarios
    
    Forecast_Path_Scenario1 = 'pages\\Forecasts\\dfToEdit_Scenario1.csv'
    Forecast_Path_Scenario2 = 'pages\\Forecasts\\dfToEdit_Scenario2.csv'
    Forecast_Path_Scenario3 = 'pages\\Forecasts\\dfToEdit_Scenario3.csv'

    # Read Input Data File
    df  = pd.read_excel(io = input_data_file, sheet_name = 'BBDD')
    model_data = pd.read_excel(io = input_data_file, sheet_name = 'Model')

    # Generate CheckBox - Start New Forecast
    startForecast_container = st.container(border = True)

    with startForecast_container:
        # Instructions for the user
        st.warning('Start Forecast. Select the date up to which you want to run the Forecast')

        ## Calculate the last date of the Input Database
        # Transform string format dates to datetime format
        dfDates = df
        dfDates[time_variable_str] = pd.to_datetime(dfDates[time_variable_str])

        # Calculate and store the last date
        max_date = str(df[time_variable_str].max())
        max_date = max_date[:max_date.find(' ')]

        ## Time to ask the user for the desired last date to run the Forecast
        # Form to ask for the date
        with st.form(key = 'Forecast Form'):
            
            # Date input to ask for the date.
            toDate = st.date_input(label = 'Run Forecast Until Date:', format = 'YYYY-MM-DD', value = datetime.strptime(max_date, '%Y-%m-%d'))
            # Submit button to Generate the Forecast table until the user's desired date
            submitButton = st.form_submit_button(label = 'Generate Forecast Table')

            ## Forecast table generation
            # Calculations have to be made. The user's date is checked to see if it matches the Weekday of the Input Database or not.
            # If it doesn't match we need to make it match.
            # For example if the Input Database's days are Mondays, and the user selects a Wednesday, then the Forecast will be ran until the next Moday
            if submitButton:
                # Start a list in which dates will be stored
                dateRows = []

                ## Check if the selected date is valid. It has to be a date in the future.
                # The date is valid, it is bigger than the last day of the Input Database
                if datetime.strptime(str(toDate), '%Y-%m-%d') > datetime.strptime(max_date, '%Y-%m-%d'):
                    # Store the user's desired date as the max date to calculate
                    calcDate = max_date

                    # Calculate the difference of days between the Max date and the Date selected by the user
                    dateDiff = datetime.strptime(str(toDate), '%Y-%m-%d') - datetime.strptime(max_date, '%Y-%m-%d')

                    # If the difference is a multiple of 7 is OK. If not we have to add enough days to make it OK
                    if dateDiff.days % 7 != 0:
                        toDate = str(datetime.strptime(str(toDate), '%Y-%m-%d') + timedelta(days = (7 - (dateDiff.days % 7))))
                        toDate = toDate[:toDate.find(' ')]

                    # Populate the dates list with all the dates between the last Input Database's date and the date selected by the user
                    while str(calcDate) != str(toDate):
                        # Convert calcDate to datetime format
                        calcDate = datetime(int(calcDate[:4]), int(calcDate[5:7]), int(calcDate[8:]))
                        
                        # Add 7 days to calcDate
                        calcDate = str(calcDate + timedelta(days = 7))[:str(calcDate).find(' ')]

                        # Append to columns list
                        dateRows.append(calcDate)
                    

                    # Start a DataFrame with the Independent Variables, it's groups and it's units only.
                    # model_data_aux = model_data.drop(['Fechas', 'Dependiente', 'Baseline'], axis = 1)
                    # Keep only the Independent Variales with Forcastable Groups
                    print(independent_variables_list)
                    # st.write(str(independent_variables_list))
                    model_data_aux = model_data[model_data['Variables'].isin(independent_variables_list)]
                    model_data_aux = model_data_aux[model_data_aux['Grupo'] != 'Calendar']
                    model_data_aux = model_data_aux[model_data_aux['Grupo'] != 'Other']

                    # Extract the Independent Variables and the Units as lists
                    independients = independent_variables_list
                    units = model_data_aux['Unidades'].to_list()

                    # Start the Forecast Headers by adding the Weeks header.
                    forecastTableHeaders = [time_variable_str]

                    # Add the rest of the headers with their units to make it easier to the User
                    for i,u in zip(independients, units):
                        forecastTableHeaders.append(i + '(' + u + ')')

                    # Generate forecast table with the desired headers
                    forecastTable = pd.DataFrame(columns = forecastTableHeaders)

                    # Add rows for each date
                    forecastTable[time_variable_str] = dateRows

                    # Save 3 Scenarios
                    forecastTable.to_csv(Forecast_Path_Scenario1, index = False)
                    forecastTable.to_csv(Forecast_Path_Scenario2, index = False)
                    forecastTable.to_csv(Forecast_Path_Scenario3, index = False)

                    st.success('Forecast table is created. You can edit it selecting Edit Forecast')

                # The date is not valid
                else:
                    st.error('Please select a date bigger than ' + max_date)

    if (os.path.exists(Forecast_Path_Scenario1)) and (os.path.exists(Forecast_Path_Scenario2)) and (os.path.exists(Forecast_Path_Scenario3)):
        st.warning('An old Forecast Table exists. If you want to continue editing it click "Edit Forecast". If you want to create a new one, click "Start Forecast" and generate a new table')

        # Generate CheckBox - Start New Forecast
        editForecast_container = st.container(border = True)

        # If the user wants to edit the Scenarios
        with editForecast_container:

            # Instructions for the user
            st.warning('Edit Forecast Scenarios. Add all the desired values to the Forecast tables and click save Forecast.')

            # Scenario 1 Edit table
            st.subheader('Scenario 1')

            st.write('Fill in the expected invest for each marketing variable:')
            forecastTable_Scenario1 = pd.read_csv(Forecast_Path_Scenario1)
            forecastTable_Scenario1 = st.data_editor(data = forecastTable_Scenario1, key = 'Scenario 1')

            # Scenario 1 values for outcome
            forecastHeaders = []
            forecastHeaders = forecastTable_Scenario1.columns.to_list()

            scenario_est_costs_columns = ['Category']
            for header in forecastHeaders:
                if header == time_variable_str:
                    pass
                else:
                    scenario_est_costs_columns.append(header)


            scenario1_est_costs_df = pd.DataFrame(columns = scenario_est_costs_columns)
            scenario1_est_costs_df['Category'] = ['Estimated Cost']

            st.write('Fill in the estimated cost per marketing variable unit')
            scenario1_est_costs_table = st.data_editor(scenario1_est_costs_df, key = 'Scenario 1 Estimated Costs')

            st.write('Fill in the estimated revenue per "' + dependent_variable_str + '"')

            scenario1_est_generated_revenue = st.text_input(label = 'Estimated revenue per "' + dependent_variable_str + '"',
                                                key = 'Scenario 1 estimated revenue')
            
            try:
                float(scenario1_est_generated_revenue)
            except:
                if scenario1_est_generated_revenue == '':
                    pass
                else:
                    st.error('Error. Must be a number with decimals after a .')

            # Scenario 2 Edit Table
            st.subheader('Scenario 2')
            forecastTable_Scenario2 = pd.read_csv(Forecast_Path_Scenario2)
            forecastTable_Scenario2 = st.data_editor(data = forecastTable_Scenario2, key = 'Scenario 2')
            
            # Scenario 2 values for outcome
            
            scenario2_est_costs_df = pd.DataFrame(columns = scenario_est_costs_columns)
            scenario2_est_costs_df['Category'] = ['Estimated Cost']

            st.write('Fill in the estimated cost per marketing variable unit')
            scenario2_est_costs_table = st.data_editor(scenario2_est_costs_df, key = 'Scenario 2 Estimated Costs')

            st.write('Fill in the estimated revenue per "' + dependent_variable_str + '"')

            scenario2_est_generated_revenue = st.text_input(label = 'Estimated revenue per "' + dependent_variable_str + '"',
                                                key = 'Scenario 2 estimated revenue')
            
            try:
                float(scenario2_est_generated_revenue)
            except:
                if scenario2_est_generated_revenue == '':
                    pass
                else:
                    st.error('Error. Must be a number with decimals after a .')
            
            # Scenario 3 Edit Table
            st.subheader('Scenario 3')
            forecastTable_Scenario3 = pd.read_csv(Forecast_Path_Scenario3)
            forecastTable_Scenario3 = st.data_editor(data = forecastTable_Scenario3, key = 'Scenario 3')

            # Scenario 3 values for outcome
            
            scenario3_est_costs_df = pd.DataFrame(columns = scenario_est_costs_columns)
            scenario3_est_costs_df['Category'] = ['Estimated Cost']

            st.write('Fill in the estimated cost per marketing variable unit')
            scenario3_est_costs_table = st.data_editor(scenario3_est_costs_df, key = 'Scenario 3 Estimated Costs')

            st.write('Fill in the estimated revenue per "' + dependent_variable_str + '"')

            scenario3_est_generated_revenue = st.text_input(label = 'Estimated revenue per "' + dependent_variable_str + '"',
                                                key = 'Scenario 3 estimated revenue')
            
            try:
                float(scenario3_est_generated_revenue)
            except:
                if scenario3_est_generated_revenue == '':
                    pass
                else:
                    st.error('Error. Must be a number with decimals after a .')

            # Save Forecast Scenarios button
            saveEditDfButton = st.button('Save Forecast Scenarios')

            # Save the Scenarios if the button is clicked
            if saveEditDfButton:
                forecastTable_Scenario1.to_csv(Forecast_Path_Scenario1, index = False)
                forecastTable_Scenario2.to_csv(Forecast_Path_Scenario2, index = False)
                forecastTable_Scenario3.to_csv(Forecast_Path_Scenario3, index = False)
                st.success('Forecasts Saved')
            

        generateForecast_container = st.container(border = True)

        totals_columns = ['Variable', 'Scenario 1', 'Scenario 2', 'Scenario 3']
        totals_df = pd.DataFrame(columns = totals_columns)
        totals_headers = forecastHeaders[1:]
        totals_df[totals_columns[0]] = totals_headers

        with generateForecast_container:
                        
            st.warning('Forecast Charts. Here you can see the different forecasts results')
            
            for i in range(3):
            
                # Read Forecast table
                if i == 0:
                    forecastTable = pd.read_csv(Forecast_Path_Scenario1)
                if i == 1:
                    forecastTable = pd.read_csv(Forecast_Path_Scenario2)
                if i == 2:
                    forecastTable = pd.read_csv(Forecast_Path_Scenario3)

                # Read data from original Database
                df = pd.read_excel(io = input_data_file, sheet_name= 'BBDD')
                model_data = pd.read_excel(io = input_data_file, sheet_name = 'Model')

                # Get list of independent variables
                # independent_variables = model_data['Independientes'].to_list()

                # Get list of Forecast Headers
                forecastHeaders = list(forecastTable.columns)

                # Start auxiliar lists
                # Auxiliar list for Complete Forecast table. With forecasted columns and the rest of the model columns
                newForecastHeaders = []
                # Auxiliar list to find the independent variables that are not included in the forecast (Calendar variables...)
                independentNotIncluded = []

                # Delete units from headers to match the model variable names. Units are added to help the user
                for fh in forecastHeaders:
                    if fh.find('(') > -1:
                        newForecastHeaders.append(fh[:fh.find('(')])
                    else:
                        newForecastHeaders.append(fh)

                # Add the independent variables that go in the model but are not forecastable.
                for iv in independent_variables_list:
                    if iv not in newForecastHeaders:
                        newForecastHeaders.append(iv)
                        independentNotIncluded.append(iv)

                # Start Forecast table that will go in the model
                forecast = pd.DataFrame(columns = newForecastHeaders)

                # Add Forecasted values by the to the Forecast table that will go into de Model
                for fh in forecastHeaders:
                    if fh.find('(') > -1:
                        forecast[fh[:fh.find('(')]] = forecastTable[fh]
                    else:
                        forecast[fh] = forecastTable[fh]

                ## We need to find the new week values by checking the past years week values

                # Get Forecast weeks in a list
                dates = forecast[time_variable_str].to_list()

                # Find the first date of the database and extract the year
                firstDate = (df[time_variable_str][1])
                firstYear = firstDate.year

                # Loop all dates to find the similar week
                index = 0
                for date in dates:
                    # Format as date
                    date = datetime.strptime(date,'%Y-%m-%d')
                    
                    # Generate past date from forecasted date
                    newDate = str(firstYear) + '-' + str(date.month) + '-' + str(date.day)

                    # Filter database with date to get desired week
                    filtered_df = df[df[time_variable_str] <= newDate]
                    try:
                        ############# Test this case
                        print(filtered_df[time_variable_str][0])
                    except:
                        newDate = str(firstYear + 1) + '-' + str(date.month) + '-' + str(date.day)
                        newDate = datetime.strptime(newDate,'%Y-%m-%d')
                        filtered_df = df[df[time_variable_str] <= newDate]
                        filtered_df = filtered_df[filtered_df[time_variable_str] > (newDate - timedelta(days = 7))]
                    
                    # print(filtered_df)
                    # Get filtered row id
                    row_id = filtered_df.index[0]
                
                    ## To update the Forecast with the values from the filtered date we need to create a dictionary with the values
                    # Start the dictionary
                    newValues = {}

                    # Fill the dictionary with the values
                    for ini in independentNotIncluded:
                        newValues[ini] = filtered_df.loc[row_id, ini]

                    # Add the values to the Forecast row
                    forecast.loc[index, independentNotIncluded] = newValues

                    index += 1

                # print(forecast)
                    
                # Prepare Independent Variables Values to predict
                X = sm.add_constant(forecast[independent_variables_list], has_constant = 'add')

                # Predict values with model
                predictedValues = model.predict(X)

                # print(predictedValues)

                # Prepare Forecasted Dataframe.
                forecastedColumns = [time_variable_str, 'Type', dependent_variable_str]
                forecasted_df = pd.DataFrame(columns = forecastedColumns)

                # Populate Forecasted DataFrame.
                forecasted_df[time_variable_str] = dates
                forecasted_df['Type'] = 'Scenario ' + str(i + 1)
                forecasted_df[dependent_variable_str] = predictedValues

                # Concatenate modelvsreal and forecasted
                if i == 0:
                    modelVsRealVsForecast = pd.concat([modelVsReal, forecasted_df], ignore_index = True)
                else:
                    modelVsRealVsForecast = pd.concat([modelVsRealVsForecast, forecasted_df], ignore_index = True)

                # for head in forecastHeaders:

                forecast_totals = {}
                for header in forecastHeaders:
                    if header == time_variable_str:
                        forecast_totals[header] = 'Totals'
                    else:
                        forecast_totals[header] = forecastTable[header].sum()

                forecastTable.loc[len(forecastTable)] = forecast_totals
                
                for header in forecastHeaders:
                    if header == time_variable_str:
                        pass
                    else:
                        totals_df.loc[totals_df['Variable'] == header,'Scenario ' + str(i + 1)] = forecast_totals[header]
                        

            # st.table(totals_df)
            # Generate Model vs Actual line graph
            lineChart = px.line(data_frame = modelVsRealVsForecast, x = time_variable_str, y = dependent_variable_str, title = 'Forecast Chart', labels = 'Type', line_group='Type', color = 'Type', color_discrete_sequence = ['red', 'blue', 'orange', 'green', 'black'])
    
            with st.container(border = True):
                st.plotly_chart(figure_or_data = lineChart, use_container_width = True)
            
            with st.container(border = True):
                try:
                    # Calculate the 3 scenarios sum of 
                    scenario1_generated_sum = modelVsRealVsForecast[modelVsRealVsForecast['Type'] == 'Scenario 1'][dependent_variable_str].sum()
                    scenario2_generated_sum = modelVsRealVsForecast[modelVsRealVsForecast['Type'] == 'Scenario 2'][dependent_variable_str].sum()
                    scenario3_generated_sum = modelVsRealVsForecast[modelVsRealVsForecast['Type'] == 'Scenario 3'][dependent_variable_str].sum()
                    
                    forecasts_outcome_columns = ['Category', 'Scenario 1', 'Scenario 2', 'Scenario 3']
                    forecasts_outcome_categories = [str(dependent_variable_str) + ' generated', 'Cost', 'Revenue', 'ROIM']

                    forecasts_outcome_df = pd.DataFrame(columns = forecasts_outcome_columns)

                    # Add values to Category column
                    forecasts_outcome_df[forecasts_outcome_columns[0]] = forecasts_outcome_categories

                    # Add values to generated row
                    forecasts_outcome_df.at[0, forecasts_outcome_columns[1]] = round(scenario1_generated_sum,0)
                    forecasts_outcome_df.at[0, forecasts_outcome_columns[2]] = round(scenario2_generated_sum,0)
                    forecasts_outcome_df.at[0, forecasts_outcome_columns[3]] = round(scenario3_generated_sum,0)
                
                
                    # Add values to costs row

                    scenario1_total_cost = 0
                    scenario2_total_cost = 0
                    scenario3_total_cost = 0

                    for header in forecastHeaders:
                        if header == time_variable_str:
                            pass
                        else:
                            scenario1_total_cost += float(totals_df.loc[totals_df['Variable'] == header, 'Scenario 1'].values[0]) * float(scenario1_est_costs_table.at[0, header])
                            scenario2_total_cost += float(totals_df.loc[totals_df['Variable'] == header, 'Scenario 2'].values[0]) * float(scenario2_est_costs_table.at[0, header])
                            scenario3_total_cost += float(totals_df.loc[totals_df['Variable'] == header, 'Scenario 3'].values[0]) * float(scenario3_est_costs_table.at[0, header])

                    forecasts_outcome_df.at[1, forecasts_outcome_columns[1]] = scenario1_total_cost
                    forecasts_outcome_df.at[1, forecasts_outcome_columns[2]] = scenario2_total_cost
                    forecasts_outcome_df.at[1, forecasts_outcome_columns[3]] = scenario3_total_cost

                    
                    # Add values to revenue row
                    forecasts_outcome_df.at[2, forecasts_outcome_columns[1]] = round(float(scenario1_est_generated_revenue) * float(forecasts_outcome_df.at[0, forecasts_outcome_columns[1]]),0)
                    forecasts_outcome_df.at[2, forecasts_outcome_columns[2]] = round(float(scenario2_est_generated_revenue) * float(forecasts_outcome_df.at[0, forecasts_outcome_columns[2]]),0)
                    forecasts_outcome_df.at[2, forecasts_outcome_columns[3]] = round(float(scenario3_est_generated_revenue) * float(forecasts_outcome_df.at[0, forecasts_outcome_columns[3]]),0)

                    # Add ROIM values
                    forecasts_outcome_df.at[3, forecasts_outcome_columns[1]] = str(round(((float(forecasts_outcome_df.at[2, forecasts_outcome_columns[1]]) - float(forecasts_outcome_df.at[1, forecasts_outcome_columns[1]])) / float(forecasts_outcome_df.at[1, forecasts_outcome_columns[1]])) * 100,2)) + ' %'
                    forecasts_outcome_df.at[3, forecasts_outcome_columns[2]] = str(round(((float(forecasts_outcome_df.at[2, forecasts_outcome_columns[2]]) - float(forecasts_outcome_df.at[1, forecasts_outcome_columns[2]])) / float(forecasts_outcome_df.at[1, forecasts_outcome_columns[2]])) * 100,2)) + ' %'
                    forecasts_outcome_df.at[3, forecasts_outcome_columns[3]] = str(round(((float(forecasts_outcome_df.at[2, forecasts_outcome_columns[3]]) - float(forecasts_outcome_df.at[1, forecasts_outcome_columns[3]])) / float(forecasts_outcome_df.at[1, forecasts_outcome_columns[3]])) * 100,2)) + ' %'

                    # Show Forecasts Outcome Table
                    st.table(forecasts_outcome_df)
                
                    charts_df = forecasts_outcome_df[forecasts_outcome_df['Category'].isin([dependent_variable_str + ' generated', 'ROIM'])]

                    for col in ['Scenario 1', 'Scenario 2', 'Scenario 3']:
                        charts_df[col] = charts_df[col].replace({' %': ''}, regex = True)
                        charts_df[col] = pd.to_numeric(charts_df[col], errors = 'coerce')
                    
                    charts_df = charts_df.melt(id_vars = 'Category', var_name = 'Scenario', value_name = 'Value')

                    # st.table(charts_df)

                    bar_chart_df = charts_df[charts_df['Category'] == dependent_variable_str + ' generated']
                    line_chart_df = charts_df[charts_df['Category'] == 'ROIM']

                    generated_column, roim_column = st.columns(2)

                    with generated_column.container(border = True):
                        generated_chart = px.bar(data_frame = bar_chart_df, x = 'Scenario', y = 'Value', color = 'Scenario', title = 'Forecast Outcome', labels = {'Value' : dependent_variable_str + ' generated'}, color_discrete_sequence = ['orange', 'green', 'black'])
                        st.plotly_chart(figure_or_data = generated_chart, use_container_width = True)

                    with roim_column.container(border = True):
                        roim_chart = px.line(data_frame = line_chart_df, x = line_chart_df['Scenario'], y = line_chart_df['Value'], title = 'Forecasted ROIMs (%)')
                        st.plotly_chart(figure_or_data = roim_chart, use_container_width = True)
                except:
                    st.warning('Introduce values for Costs and Revenues for each scenario')

                

                
                

                



