import streamlit as st
import pandas as pd
from dateutil import parser
import pages.NaawaNexus_Functions_LinearRegression as NaawaNexus_Functions_LinearRegression
import statsmodels.api as sm
import plotly.express as px

# To parametrize
supported_file_extensions_list = ['xls', 'xlsx']

def Page_Modelling(languaje):
    ## Modelling Page function
    # Title and Header
    if languaje == 'ENG':
        st.title(body = 'Modelling')
        st.subheader(body = 'Conect your data and create your own business demand models. Find out which is the best possible fit for your dataset')
    elif languaje == 'SPA':
        st.title(body = 'Modelling')
        st.subheader(body = 'Introduzca la base de datos para correr modelos de Regresión Lineal y ver qué factores impactan en la Demanda Incremental de su negocio')
    
    # File uploader
    input_data_file = st.file_uploader('File uploader')

    # Actions if file is loaded
    if input_data_file is not None:

        # Extract File Name and File Extension
        file_name_str = input_data_file.name
        file_extension_str = file_name_str[file_name_str.find('.') + 1:]
        
        # Check if File Extension is correct.
        # If file extension is not correct show an error
        if file_extension_str not in supported_file_extensions_list:
            if languaje == 'ENG':
                extension_error_body_str = "File Extension '" + file_extension_str + "' is not correct. Must be one of these: csv, xls, xlsx."
            elif languaje == 'SPA':
                extension_error_body_str = "La extensión del fichero '" + file_extension_str + "' no es correcta. Debe ser una de estas: csv, xls, xlsx."
            
            st.error(body = extension_error_body_str)
                    
        # If file extension is correct start modelling
        else:
            st.session_state.input_data_file = input_data_file

            #try:
            # First, the data must be read
            if file_extension_str == 'csv':
                data_df = pd.read_csv(input_data_file)
            elif (file_extension_str == 'xls') or (file_extension_str == 'xlsx'):
                data_df = pd.read_excel(input_data_file, sheet_name = 'ddbb')
            #except:
            #    if languaje == 'ENG':
            #        st.error('Make sure a sheet with the data exists and it is named "BBDD"')
            #    elif languaje == 'SPA':
            #        st.error('Asegurate que existe una hoja con datos llamada "BBDD"')

            # Read data's columns
            columns_list = data_df.columns.to_list()

            # Second, the user must select type of Modelling: Best possible or manual selection of variables
            if languaje == 'ENG':
                type_options_list = ['Manual Variable Selection','Best Possible Model']
                type_options_popover = st.popover('Select how to create the model')
                type_option = type_options_popover.radio(label = 'Select how to create the model', options = type_options_list, index = None)
            elif languaje == 'SPA':
                type_options_list = ['Selección Manual de Variables','Mejor modelo posible']
                type_options_popover = st.popover('Seleccione forma de hacer el modelo')
                type_option = type_options_popover.radio(label = 'Seleccione forma de hacer el modelo', options = type_options_list, index = None)

            # If the user wants to Model manually
            if type_option == type_options_list[0]:
                try:
                    
                    st.session_state.time_variable_str = ''
                    st.session_state.model = None
                    st.session_state.modelVsReal = None
                    st.session_state.dependent_variable_str = ''
                    st.session_state.independent_variables_list = []

                    # Run Manual Model Function to get the desired model, and also the Dependent, Independent and Time variables for further actions
                    model, dependent_variable_str, independent_variables_list, time_variable_str = NaawaNexus_Functions_LinearRegression.runManuallySelectedModel(data_df = data_df, columns_list = columns_list, languaje = languaje)

                    # Generate Model Vs Real DataFrame from the model obtained in the previous step
                    modelVsReal = NaawaNexus_Functions_LinearRegression.generateActualVsModel(data_df = data_df, model = model, dependent_variable_str = dependent_variable_str, independent_variables_list = independent_variables_list, time_variable_str = time_variable_str)

                    # Filter Model Vs Real DataFrame to get only the Model and Actual Values
                    condition = (modelVsReal['Type'].isin(['Model', 'Actual']))
                    df_modelVSactual = modelVsReal[condition]

                    # Generate Model vs Actual line graph
                    lineChart = px.line(data_frame = df_modelVSactual, x = time_variable_str, y = dependent_variable_str, title = 'Model Vs Actual Chart', labels = 'Type', line_group='Type', color = 'Type', color_discrete_sequence = ['red', 'blue'])
                    
                    # Plot the chart in the app
                    with st.container(border = True):
                        st.plotly_chart(figure_or_data = lineChart, use_container_width = True)
                    
                    # Generate Attribution Data DataFrame from the model obtained above
                    attribution_data_df = NaawaNexus_Functions_LinearRegression.getAttributionData(data_df = data_df, dependent_variable_str = dependent_variable_str, independent_variables_list = independent_variables_list, time_variable_str = time_variable_str, model = model, languaje = languaje)

                    # Get Attribution Data Columns to extract the variables to plot
                    attribution_data_columns = attribution_data_df.columns.to_list()

                    # Generate Attribution Data Chart
                    attribution_data_bar_chart = px.bar(data_frame = attribution_data_df, x = time_variable_str, y = attribution_data_columns[1:], title = 'Model Composition Chart')

                    # Plot the chart in the app
                    with st.container(border = True):
                        st.plotly_chart(figure_or_data = attribution_data_bar_chart, use_container_width = True)
                    
                    st.session_state.time_variable_str = time_variable_str
                    st.session_state.model = model
                    st.session_state.modelVsReal = modelVsReal
                    st.session_state.dependent_variable_str = dependent_variable_str
                    st.session_state.independent_variables_list = independent_variables_list

                    # NaawaNexus_Page_Outcome.Page_Outcome(languaje = languaje, model = model, input_data_file = input_data_file, dependent_variable_str = dependent_variable_str, independent_variables_list = independent_variables_list, time_variable_str = time_variable_str)

                except:
                    if languaje == 'ENG':
                        st.warning("Model's summary will appear here once you have selected the variables to run it")
                    elif languaje == 'SPA':
                        st.warning('El resumen de su modelo aparecerá aquí abajo una vez haya seleccionado las variables para el mismo')

            elif type_option == type_options_list[1]:
                try:

                    st.session_state.time_variable_str = ''
                    st.session_state.model = None
                    st.session_state.modelVsReal = None
                    st.session_state.dependent_variable_str = ''
                    st.session_state.independent_variables_list = []

                    # Run Best Possible Model Function to get the best model, and also the Dependent, Independent and Time variables for further actions
                    best_model, dependent_variable_str, best_independent_variables_list, time_variable_str = NaawaNexus_Functions_LinearRegression.runBestPossibleModel(data_df = data_df, columns_list = columns_list, languaje = languaje)

                    # Generate Model Vs Real DataFrame from the model obtained in the previous step
                    best_modelVsReal = NaawaNexus_Functions_LinearRegression.generateActualVsModel(data_df = data_df, model = best_model, dependent_variable_str = dependent_variable_str, independent_variables_list = best_independent_variables_list, time_variable_str = time_variable_str)
                    
                    # Filter Model Vs Real DataFrame to get only the Model and Actual Values
                    condition = (best_modelVsReal['Type'].isin(['Model', 'Actual']))
                    df_best_modelVSactual = best_modelVsReal[condition]
                    
                    # Generate Model vs Actual line graph
                    best_lineChart = px.line(data_frame = df_best_modelVSactual, x = time_variable_str, y = dependent_variable_str, title = 'Model Vs Actual Chart', labels = 'Type', line_group='Type', color = 'Type', color_discrete_sequence = ['red', 'blue'])

                    # Plot the chart in the app
                    with st.container(border = True):
                        st.plotly_chart(figure_or_data = best_lineChart, use_container_width = True)

                    # Generate Attribution Data DataFrame from the model obtained above
                    best_attribution_data_df = NaawaNexus_Functions_LinearRegression.getAttributionData(data_df = data_df, dependent_variable_str = dependent_variable_str, independent_variables_list = best_independent_variables_list, time_variable_str = time_variable_str, model = best_model, languaje = languaje)
                    
                    # Get Attribution Data Columns to extract the variables to plot
                    best_attribution_data_columns = best_attribution_data_df.columns.to_list()
                    
                    # Generate Attribution Data Chart
                    bar_chart = px.bar(data_frame = best_attribution_data_df, x = time_variable_str, y = best_attribution_data_columns[1:], title = 'Model Composition Chart')
                    
                    # Plot the chart in the app
                    with st.container(border = True):
                        st.plotly_chart(figure_or_data = bar_chart, use_container_width = True)

                    # NaawaNexus_Page_Outcome.Page_Outcome(languaje = languaje, model = best_model, input_data_file = input_data_file, dependent_variable_str = dependent_variable_str, independent_variables_list = best_independent_variables_list, time_variable_str = time_variable_str)
                    st.session_state.time_variable_str = time_variable_str
                    st.session_state.model = best_model
                    st.session_state.modelVsReal = best_modelVsReal
                    st.session_state.dependent_variable_str = dependent_variable_str
                    st.session_state.independent_variables_list = best_independent_variables_list
                    
                except:
                    if languaje == 'ENG':
                        st.warning("Model's summary will appear here once you have selected the variables to run it")
                    elif languaje == 'SPA':
                        st.warning('El resumen de su modelo aparecerá aquí abajo una vez haya seleccionado las variables para el mismo')
                
            else:
                if languaje == 'ENG':
                    st.warning(body = 'Select a method to run the model to continue')
                elif languaje == 'SPA':
                    st.warning(body = 'Seleccione una forma de hacer el modelo para continuar')
            
            
    
    else:
        if languaje == 'ENG':
            st.warning("Please load a file to start the analysis")
        elif languaje == 'SPA':
            st.warning('Por favor cargue un fichero para empezar el análisis')
    
    




        


