import streamlit as st
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.outliers_influence import variance_inflation_factor
import pandas as pd
from itertools import combinations

independent_variables_aux_list = []
columns_list: list
combinations_limit = 10

def runLinearRegressionModel(data_df, dependent_variable_str, independent_variables_list):
    ## Function to calculate a Linear Regression Model
    # Inputs are the Data DataFrame, the Dependent Variable as string, and the list of independent variables

    # Independent variables for the model with a constant term for the intercept
    X = sm.add_constant(data_df[independent_variables_list])

    # Dependent variable
    Y = data_df[dependent_variable_str]

    # Fit the linear regression model
    model = sm.OLS(Y, X).fit()

    # Calculate VIF for al model's variables
    vif_data = pd.DataFrame()
    vif_data["Variable"] = X.columns
    vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    
    # Calculate VIF mean
    mean_vif = vif_data['VIF'].mean()
    
    # Outputs are the model and the VIF mean value
    return model, mean_vif

def runLinearRegressionModelFromFormula(data_df, dependent_variable_str, independent_variables_list):
    ## Function to calculate a Linear Regression Model but the variables are a formula
    # Inputs are the Data DataFrame, the Dependent Variable as string, and the list of independent variables
    
    # Start formula
    formula = ''

    # Add dependent variable to formula
    formula = formula + dependent_variable_str + ' ~ '

    # Add independent variables to formula
    for independent_variable in independent_variables_list:
        formula = formula + ' + ' + independent_variable
    
    # Fit the linear regression model from formula    
    model = ols(formula = formula,data = data_df).fit()
    
    # Output is the model
    return model

def testANOVAsignificancy(model):
    ## Function to see if all the variables are significant in ANOVA test
    # Input is the model ran previously

    # Generate ANOVA table from the model
    anova = sm.stats.anova_lm(model, typ=2) # Type 2 Anova DataFrame

    # Iterate al rows to check the significancy
    for index, row in anova.iterrows():
        if (pd.isna(row['PR(>F)'])) or (row['PR(>F)'] <= 0.05):
            ANOVAresult = 'OK'
        else:
            ANOVAresult = 'KO'
            break
    
    # Output is a string to say if all the ANOVA significancies are ok or not
    return ANOVAresult

def getModelFormula(model, dependent_variable_str, independent_variables_list):
    ## Funtion to generate a string with the Model parameter's formula
    # Inputs are the model, the dependent variable as string, and the list of independent variables

    # Extract the Model Parameters
    params = model.params

    # Start Formula by adding the Dependent variable, an equal and the constant value. Example: Dependent = XX.XX
    formula = str(dependent_variable_str) + '=' + str(round(params['const'],2))

    # Generate a variable to check how many characters have been added to the formula and insert a new line to make it visible in the page
    last_values = formula

    # Add each Independent Variable's coefficients to formula
    for ind_var in independent_variables_list:
        ind_var: str
        # If coefficient is positive add it with a + sign
        if params[ind_var] >= 0:
            formula = formula + ' + ' + str(round(params[ind_var],2)) + '*' + str(ind_var)
            last_values = last_values + ' + ' + str(round(params[ind_var],2)) + ' ' + str(ind_var)
        # I coefficient is negative don't add sign because it already brings it
        else:
            formula = str(formula) + str(round(params[ind_var],2)) + '*' + str(ind_var)
            last_values = last_values + str(round(params[ind_var],2)) + ' ' + str(ind_var)
        
        # If over 20 characters have been added to the formula add a new line
        if len(last_values) >= 20:
            formula = formula + (r'''\newline''')
            last_values = ''
        else:
            pass
    
    # Add escape character to _ so it is correctly shown in the app
    formula = r'''''' + formula.replace('_','\_')
    
    # Output is the formula's string
    return formula

def getLinearRegressionModelStatistics(model, data_df, mean_vif):
    ## Function to calculate some statistics from a Linear Regression Model
    # Inputs are the model, the Data DataFrame and the VIF mean
    
    # Calculate R-Squared and R-Squared-Adj
    rsquared = model.rsquared
    rsquared_adj = model.rsquared_adj

    # Durbin-Watson statistic
    durbin_watson = sm.stats.stattools.durbin_watson(model.resid)

    # Add the statistics to the output dictionary
    statistics = {
        "rsquared" : rsquared,
        "adjusted rsquared" : rsquared_adj,
        "mean vif" : mean_vif,
        "durbin watson" : durbin_watson
    }

    # Output is a dictionary with the statistics calculated
    return statistics

def runManuallySelectedModel(data_df, columns_list, languaje):
    ## Function to generate all the actions for the user tu run a model selecting manually all the Variables
    # Page header if languajes are English or Spanish
    if languaje == 'ENG':
        st.header('Run Model manually selecting the Independent Variables')
        st.text('You will have to select the Dependent Variable, the Independent Variables and the Time variable in the Database')

        # The user must say which are the dependent and independent variables
        st.subheader(body = 'Select the Dependent Variable, the Independent Variables and the Time variable')
    elif languaje == 'SPA':
        st.header('Modelo seleccionando manualmente las variables independientes')
        st.text('Usted deberá seleccionar la variable dependiente, las variables independientes, y la variable temporal de la base de datos')

        # The user must say which are the dependent and independent variables
        st.subheader(body = 'Seleccione la variable dependiente y las variables independientes')
    
    # Popovers to select the Variables that will define the model
    
    if languaje == 'ENG':
        # Dependent variable. Choose only one from the list
        dependent_variable_popover = st.popover('Select Dependent Variable')
        dependent_variable_str = dependent_variable_popover.radio(label = 'Select Dependent Variable', options = columns_list, index = None)
    
    elif languaje == 'SPA':
        # Dependent variable. Choose only one from the list
        dependent_variable_popover = st.popover('Seleccione Variable Dependiente')
        dependent_variable_str = dependent_variable_popover.radio(label = 'Seleccione Variable Dependiente', options = columns_list, index = None)
    
    if dependent_variable_str is not None:
        # Time variable. Choose only one from the list
        time_variables_list = []

        # Generate possible variables list
        for column in columns_list:
            # Add variable to list if it is not the Dependent Variable chosen before
            if (column != dependent_variable_str) and (column not in time_variables_list):
                time_variables_list.append(column)
            else:
                pass
        
        # Popovers to select Time and Independent variables
        if languaje == 'ENG':
            # Time variables. Choose only one, except the one that was selected as Dependent variable
            time_variable_popover = st.popover('Select Time Variable')
            time_variable_str = time_variable_popover.radio(label = 'Select Time Variable', options = time_variables_list, index = None)

            # Independent variables. Choose as many as possible, except the ones that were selected as Dependent variable and Time Variables
            independent_variables_popover = st.popover('Select Independent Variable')
        elif languaje == 'SPA':
            # Time variables. Choose only one, except the one that was selected as Dependent variable
            time_variable_popover = st.popover('Seleccione Variable Temporal')
            time_variable_str = time_variable_popover.radio(label = 'Seleccione Variable Temporal', options = time_variables_list, index = None)

            # Independent variables. Choose as many as possible, except the ones that were selected as Dependent variable and Time Variables
            independent_variables_popover = st.popover('Seleccione Variable Independiente')
        
        # Generate popover to select Independent variables
        for column in columns_list:
            # Show but disabled the Dependent and the Time variables
            if (column == dependent_variable_str) or (column == time_variable_str):
                checkbox_value = independent_variables_popover.checkbox(column, disabled = True)
            else :
                checkbox_value = independent_variables_popover.checkbox(column)
                # Add variable to Independent Variables list or not.
                if (checkbox_value == True)and (column not in independent_variables_aux_list):
                    independent_variables_aux_list.append(column)
                elif (checkbox_value == False) and (column in independent_variables_aux_list):
                    independent_variables_aux_list.remove(column)
                else:
                    pass
                    
        # An auxiliary list is created to generate the list of independent variables
        independent_variables_list = independent_variables_aux_list

        # Show Variables
        if languaje == 'ENG':
            # Show Dependent Variable
            st.subheader(body = 'Dependent Variable')
            if dependent_variable_str is not None:
                st.write(dependent_variable_str)
            else:
                st.warning('Select the Dependent Variable')
            # Show Time Variable
            st.subheader(body = 'Time variable')
            if time_variable_str is not None:
                st.write(time_variable_str)
            else:
                st.warning('Select the Time Variable')
            # Show Independent Variables
            st.subheader(body = 'Independent Variables')
            if independent_variables_list:
                st.write(str(independent_variables_list).replace('[','').replace(']',''))
            else:
                st.warning('Select the Independent Variables')
        elif languaje == 'SPA':
            # Show Dependent Variable
            st.subheader(body = 'Variable Dependiente')
            if dependent_variable_str is not None:
                st.write(dependent_variable_str)
            else:
                st.warning('Seleccione una Variable Dependiente')
            # Show Time Variable
            st.subheader(body = 'Variable Temporal')
            if time_variable_str is not None:
                st.write(time_variable_str)
            else:
                st.warning('Seleccione la Variable Temporal')
            # Show Independent Variables
            st.subheader(body = 'Variables independientes')
            if independent_variables_list:
                st.write(str(independent_variables_list).replace('[','').replace(']',''))
            else:
                st.warning('Seleccione variables independientes')
        
        # Run Model if Dependent and Independent Variables are selected
        if (dependent_variable_str is not None) and (time_variable_str is not None) and (independent_variables_list != []):
            # Run Model Button
            if languaje == 'ENG':            
                model_button = st.button(label = 'Run Model')
            elif languaje == 'SPA':            
                model_button = st.button(label = 'Generar Modelo')
            # Run model when button is clicked
            if model_button:
                # Run Model with Run Linear Regression Model function. Model and Mean VIF will be returned
                model, mean_vif = runLinearRegressionModel(data_df = data_df, dependent_variable_str = dependent_variable_str, independent_variables_list = independent_variables_list)
                
                # Generate two columns to show the Model Results.
                model_overview_column, statistics_column = st.columns(2)
        
                # Show Model Overview in one column
                with model_overview_column:
                    with st.container(border = True):
                        if languaje == 'ENG':
                            st.subheader('Model Drivers')
                        elif languaje == 'SPA':
                            st.subheader('Drivers del Modelo')
                        st.table(data = model.params)
                
                # Show Model vs Actual Graph in one column
                with statistics_column:
                    with st.container(border = True):
                        if languaje == 'ENG':
                            st.subheader('Model Statistics')
                        elif languaje == 'SPA':
                            st.subheader('Estadísticas del Modelo')
                        
                        # Calculate the Model's statistics with the function built for it
                        statistics = getLinearRegressionModelStatistics(model = model, data_df = data_df, mean_vif = mean_vif)
                        
                        # Generate two columns to show the stats more clearly
                        stats_column1, stats_column2 = st.columns(2)
                        # First column will show the R squared and the Adjusted R squared statistics
                        with stats_column1:
                            # Show R squared using latex functions to write it in mathematic style
                            st.latex('R^2 = '+ str(round(statistics['rsquared'],2)))
                            # Show Adjuste dR squared using latex functions to write it in mathematic style
                            st.latex('Adjusted\,R^2 = '+ str(round(statistics['adjusted rsquared'],2)))
                        # Second column will show the Mean VIF and the Durbin Watson statistics
                        with stats_column2:
                            # Show Mean VIF using latex functions to write it in mathematic style
                            st.latex('\overline{VIF} = '+ str(round(statistics['mean vif'],2)))
                            # Show Durbin Watson using latex functions to write it in mathematic style
                            st.latex('DW = '+ str(round(statistics['durbin watson'],2)))
                    
                    # Below the statistics the Model Formula must be shown in a new container
                    with st.container(border = True):
                        if languaje == 'ENG':
                            st.subheader('Model Formula')
                        elif languaje == 'SPA':
                            st.subheader('Fórmula del Modelo')
                        # Generate Model Formula with the function built for it
                        formula = getModelFormula(model, dependent_variable_str, independent_variables_list)
                        # Show Formula using latex functions to write it in mathematic style
                        st.latex(formula)

    # Outputs of this function are the Model, and the Dependent, Time and Independent Variables.
    return model, dependent_variable_str, independent_variables_list, time_variable_str

def runBestPossibleModel(data_df, columns_list:list, languaje):
    ## Function to generate all the actions for the user tu run a model selecting manually all the Variables
    best_independent_variables_list = []
    try:
        best_model, previf = runLinearRegressionModel(data_df = data_df, dependent_variable_str = str(columns_list[2]), independent_variables_list = [columns_list[3], columns_list[4]] )
    except:
        pass
    
    # Page header if languajes are English or Spanish
    if languaje == 'ENG':
        st.header('Best possible Model')
        st.text('You will have to select the Dependent Variable, the Time Variable to be excluded from the Model, the Independent Variables you will want to obligatory include in the Model, and any Variable you want to avoid from entering the model.')
        
        # The user must say which are the dependent and independent variables
        st.subheader(body = 'Select the different values below')
    elif languaje == 'SPA':
        st.header('Mejor modelo posible')
        st.text('Usted deberá seleccionar la variable dependiente, decir cuál es la variable temporal para no incluirla en el modelo, seleccionar las variables independientes que sí o sí deben entrar en el modelo, y si quiere que alguna no entre.')

        # the user must say which are the dependent and independent variables
        st.subheader(body = 'Seleccione más abajo las variables')

    if languaje == 'ENG':
        # Dependent variable. Choose only one from the list
        dependent_variable_popover = st.popover('Select Dependent Variable')
        dependent_variable_str = dependent_variable_popover.radio(label = 'Select Dependent Variable', options = columns_list, index = None)

    elif languaje == 'SPA':
        # Dependent variable. Choose only one from the list
        dependent_variable_popover = st.popover('Seleccione Variable Dependiente')
        dependent_variable_str = dependent_variable_popover.radio(label = 'Seleccione Variable Dependiente', options = columns_list, index = None)

    if dependent_variable_str is not None:
        # Time variable. Choose only one from the list
        time_variables_list = []

        # Generate possible Time Variables list without the Dependent Variable
        for column in columns_list:
            if (column != dependent_variable_str) and (column not in time_variables_list):
                time_variables_list.append(column)
            else:
                pass
        
        # Time Variable popover
        if languaje == 'ENG':
            time_variable_popover = st.popover('Select Time Variable')
            time_variable_str = time_variable_popover.radio(label = 'Select Time Variable', options = time_variables_list, index = None)

        elif languaje == 'SPA':
            time_variable_popover = st.popover('Seleccione Variable Temporal')
            time_variable_str = time_variable_popover.radio(label = 'Seleccione Variable Temporal', options = time_variables_list, index = None)

        # Generate independent variables lists, obligatory and optional ones
        independent_variables_list = []
        for column in columns_list:
            if (column != dependent_variable_str) and (column != time_variable_str) and (column not in independent_variables_list):
                independent_variables_list.append(column)
            else:
                pass
        
        # Obligatory Independent Variables Popoover
        if languaje == 'ENG':
            obligatory_independent_variables_popover = st.popover('Select the Obligatory Independent Variables that will go into the Model')
        elif languaje == 'SPA':
            obligatory_independent_variables_popover = st.popover('Seleccione las variables independientes que deben entrar obligatoriamente en el modelo')
        
        # Generate Obligatory Independent Variables List
        obligatory_independent_variables_aux_list = []
        count = 0
        for column in columns_list:

            # Include but as disabled options the Dependant and the Time variables
            if (column == dependent_variable_str) or (column == time_variable_str):
                obligatory_checkbox_value = obligatory_independent_variables_popover.checkbox(column, disabled = True, key = count)
                count += 1
            
            # Generate auxiliary Obligatory Independent Variables List
            else :
                obligatory_checkbox_value = obligatory_independent_variables_popover.checkbox(column, key = count)
                count += 1
                # Add variable to Independent Variables list or not.
                if (obligatory_checkbox_value == True) and (column not in independent_variables_aux_list):
                    obligatory_independent_variables_aux_list.append(column)
                elif (obligatory_checkbox_value == False) and (column in independent_variables_aux_list):
                    obligatory_independent_variables_aux_list.remove(column)
                else:
                    pass
        
        # Obligatory Independent Variables List from the auxiliary one
        obligatory_independent_variables_list = obligatory_independent_variables_aux_list

        # Generate Excluded Independent Variables List
        excluded_idependent_variables_aux_list = []

        # Excluded Independent Variables Popover
        if languaje == 'ENG':
            excluded_idependent_variables_popover = st.popover('Select the Independent Variables you do not want to introduce in the Model')
        elif languaje == 'SPA':
            excluded_idependent_variables_popover = st.popover('Seleccione las variables independientes que no quiere que entren en el modelo')
        
        # Generate Auxiliary Excluded Variables List
        for column in columns_list:
            # Include disabled the Dependent, Time and obligatory Variables
            if (column == dependent_variable_str) or (column == time_variable_str) or (column in obligatory_independent_variables_list):
                checkbox_value = excluded_idependent_variables_popover.checkbox(column, disabled = True, key = count)
                count += 1
            # Select the rest of the variables
            else:
                checkbox_value = excluded_idependent_variables_popover.checkbox(column, key = count)
                count += 1
                if (checkbox_value == True) and (column not in excluded_idependent_variables_aux_list):
                    excluded_idependent_variables_aux_list.append(column)
                elif (checkbox_value == False) and (column in excluded_idependent_variables_aux_list):
                    excluded_idependent_variables_aux_list.remove(column)
                else:
                    pass

        # Excluded Independent Variables List from the auxiliary one
        excluded_independent_variables_list = excluded_idependent_variables_aux_list
        
        # Generate Optional Independent Variables List
        optional_independent_variables_list = []

        for column in columns_list:
            if (column == dependent_variable_str) or (column == time_variable_str) or (column in obligatory_independent_variables_list) or (column in excluded_independent_variables_list):
                pass
            else:
                optional_independent_variables_list.append(column)

        # Generate Final Independent Variables List, including the Obligatory and the Optionals
        final_independent_variables_list = []
        # Add obligatory variables
        for variable in obligatory_independent_variables_list:
            final_independent_variables_list.append(variable)
        # Add optional variables
        for variable in optional_independent_variables_list:
            final_independent_variables_list.append(variable)
        
        # Show the selected variables for the user to check
        if languaje == 'ENG':
            # Show Dependent Variable
            st.subheader(body = 'Dependent Variable')
            if dependent_variable_str is not None:
                st.write(dependent_variable_str)
            else:
                st.warning('Select the Dependent Variable')
            
            # Show Time Variable
            st.subheader(body = 'Time Variable')
            
            if time_variable_str is not None:
                st.write(time_variable_str)
            else:
                st.warning('Select the Time Variable')
            
            # Show Independent Variables
            if (time_variable_str is not None) and (dependent_variable_str is not None):
                st.subheader(body = 'Obligatory Independent Variables')
                st.write(str(obligatory_independent_variables_list).replace('[','').replace(']',''))
                st.subheader(body = 'Excluded Independent Variables')
                st.write(str(excluded_independent_variables_list).replace('[','').replace(']',''))
                st.subheader(body = 'Optional Independent Variables')
                st.write(str(optional_independent_variables_list).replace('[','').replace(']',''))
                
            else:
                st.warning(body = 'Once you select the Dependent and Time variables, the Independent Variables will appear here')
       
       # Show the selected variables for the user to check     
        elif languaje == 'SPA':
            # Show Dependent Variable
            st.subheader(body = 'Variable Dependiente')
            if dependent_variable_str is not None:
                st.write(dependent_variable_str)
            else:
                st.warning('Seleccione una Variable Dependiente')
            
            # Show Time Variable            
            st.subheader(body = 'Variable Temporal')
            
            if time_variable_str is not None:
                st.write(time_variable_str)
            else:
                st.warning('Seleccione una Variable Temporal')
            
            # Show Independent Variables
            if (time_variable_str is not None) and (dependent_variable_str is not None):
                st.subheader(body = 'Variables independientes Obligatorias')
                st.write(str(obligatory_independent_variables_list).replace('[','').replace(']',''))
                st.subheader(body = 'Variables independientes Excluidas')
                st.write(str(excluded_independent_variables_list).replace('[','').replace(']',''))
                st.subheader(body = 'Variables independientes Opcionales')
                st.write(str(optional_independent_variables_list).replace('[','').replace(']',''))
                
            else:
                st.warning(body = 'Una vez seleccionadas las variables dependiente y temporal, las independientes aparecerán aquí')

        # Run Best Possible Model Button
        if languaje == 'ENG':         
            best_model_button = st.button(label = 'Run Best Model')
        if languaje == 'SPA':         
            best_model_button = st.button(label = 'Generar Mejor Modelo Posible')

        # When the button is clicked
        if best_model_button:
            
            # Find the best possible Model deleting the worst significant variable one by one. The output is the list of variables that fit into that model
            best_independent_variables_list = findBestPossibleModelDeletingOneSing(data_df = data_df, 
                                                                                   dependent_variable_str = dependent_variable_str, 
                                                                                   final_independent_variables_list = final_independent_variables_list, 
                                                                                   obligatory_independent_variables_list = obligatory_independent_variables_list)
            
            # Run the model with the best possible variables
            best_model, mean_vif = runLinearRegressionModel(data_df = data_df, dependent_variable_str = dependent_variable_str, independent_variables_list = best_independent_variables_list)
            
            # Generate two columns to show the results of the model.
            best_model_overview_column, best_statistics_column = st.columns(2)

            # Generate Best Model Params Table to round the numbers and show the non significant obligatory variables
            # Start the Table
            params_table = pd.DataFrame({
                'Parameters' : best_model.params,
                'Significancy' : ''
            })
            # Round the values in the table and rename first column as index
            params_table = params_table.round(2)
            params_table.reset_index(inplace = True)

            # Extract Model Summary table. First as html, and from the html generate the DataFram
            summary = best_model.summary()
            summary_table_html = summary.tables[1].as_html()
            summary_table_df = pd.read_html(summary_table_html, header=0, index_col=0)[0]
            summary_table_df.reset_index(inplace = True)

            # Check if any of the Obligatory Independent Variables have a bad significancy
            for variable in obligatory_independent_variables_list:
                variable_data = summary_table_df[summary_table_df['index'] == variable]

                # If significancy is over 0.05 is bad
                if variable_data.iloc[0]['P>|t|'] > 0.05:
                    params_table.loc[params_table['index'] == variable, 'Significancy'] = '*'
                else:
                    pass
            
            # Rename index column as Variables
            params_table.rename(columns = {'index': 'Variables'}, inplace = True)

            # Show Model Overview in one column
            with best_model_overview_column:
                with st.container(border = True):
                    if languaje == 'ENG':
                        st.subheader('Model Drivers')
                        st.table(data = params_table.round(2).astype("str"))
                        # Add message to understand the meaning of the *
                        st.write('If a * is shown in the Significancy column it means one of the Obligatory Variables you selected may not fit precisely in the model')
                    elif languaje == 'SPA':
                        st.subheader('Drivers del Modelo')
                        # Renombrar las columnas a Español
                        params_table.rename(columns = {'Parameters': 'Parámetros', 'Significancy' : 'Significancia'}, inplace = True)
                        st.table(data = params_table.round(2).astype("str"))
                        # Add message to understand the meaning of the *
                        st.write('Si aparece un * en la columna Significancia quiere decir que una de las variables obligatorias que has escogido no encaja de forma precisa en el modelo')
            
            # Show Model vs Actual Graph in one column
            with best_statistics_column:
                # Model Statistics Container
                with st.container(border = True):
                    if languaje == 'ENG':
                        st.subheader('Model Statistics')
                    if languaje == 'SPA':
                        st.subheader('Estadísticas del Modelo')
                    
                    # Get Best Model Statistics
                    best_statistics = getLinearRegressionModelStatistics(model = best_model, data_df = data_df, mean_vif = mean_vif)

                    # Generate two columns to show the statistics
                    best_stats_column1, best_stats_column2 = st.columns(2)
                    # In column one show the R squared and the adjusted R squared
                    with best_stats_column1:
                        # Show R squared using latex functions to write it in mathematic style
                        st.latex('R^2 = '+ str(round(best_statistics['rsquared'],2)))
                        # Show Adjusted R squared using latex functions to write it in mathematic style
                        st.latex('Adjusted\,R^2 = '+ str(round(best_statistics['adjusted rsquared'],2)))
                    with best_stats_column2:
                        # Show VIF Mean using latex functions to write it in mathematic style
                        st.latex('\overline{VIF} = '+ str(round(best_statistics['mean vif'],2)))
                        # Show Durbin Watson using latex functions to write it in mathematic style
                        st.latex('DW = '+ str(round(best_statistics['durbin watson'],2)))
                # New container to show the Model Formula
                with st.container(border = True):
                    st.subheader('Model Formula')
                    # Get Best Model Formula with the function created to do it. Output is a string
                    best_formula = getModelFormula(best_model, dependent_variable_str, best_independent_variables_list)
                    # Show Model Formula in Mathematic Style
                    st.latex(best_formula)        
    
    else:
        if languaje == 'ENG':
            st.warning('Select the Dependent Variable to continue')
        elif languaje == 'SPA':
            st.warning('Seleccione la variable dependiente para continuar')
        
    # Function outputs are the Best Model's model, dependent, independent and time variables
    return best_model, dependent_variable_str, best_independent_variables_list, time_variable_str
       
def generateActualVsModel(data_df, model, dependent_variable_str, independent_variables_list, time_variable_str):
    ## Function to generate the ModelVsReal table
    # Inputs are the Data DataFrame, Dependent, Time and Independent Variables

    X = sm.add_constant(data_df[independent_variables_list])
    # Define ModelVsReal Headers
    headers = [time_variable_str,'Type', dependent_variable_str]

    # Start needed dataframes
    modelVsReal = pd.DataFrame(columns = headers)
    modelDf = pd.DataFrame(columns = headers)
    realDf = pd.DataFrame(columns = headers)

    # Generate Real data Dataframe
    realDf[time_variable_str] = data_df[time_variable_str]
    realDf['Type'] = 'Actual'
    realDf[dependent_variable_str] = data_df[dependent_variable_str]

    # Predict model values
    predicted_values = model.predict(X)

    # Generate Model data Dataframe
    modelDf[time_variable_str] = data_df[time_variable_str]
    modelDf['Type'] = 'Model'
    modelDf[dependent_variable_str] = predicted_values

    # Concatenate Dataframes to generate Model Vs Real Dataframe
    modelVsReal = pd.concat([realDf, modelDf], ignore_index = True)

    # Output is the Model Vs Actual DataFrame
    return modelVsReal

def findBestPossibleModelDeletingOneSing(data_df, dependent_variable_str, final_independent_variables_list: list, obligatory_independent_variables_list):
    ## Function to run models until the non-significant variables are taken out from the model and only the good ones remain
    # Inputs are the Data DataFRame, the Dependent, Independent (Final and Obligatory) and Time Variables
    
    # Start the All Models Row to check if the Model is good or not
    all_models_row = {
                'Dependent Variable' : dependent_variable_str,
                'Independent Variables' : [],
                'R2' : '',
                'R2Adj' : '',
                'DW' : '',
                'Sign OK' : '',
                'ANOVA OK' : '',
                'Colinealidad' : ''
    }

    # Start Model Runs Counter
    model_runs = 0

    # Run Models while the Optional Independent Variables Significancy values are not ok
    while (model_runs < 1) or (all_models_row['Sign OK'] == 'KO'):
        
        # Generate model with the Independent Variables remaining
        model, mean_vif = runLinearRegressionModel(data_df = data_df,
                                                        dependent_variable_str = dependent_variable_str,
                                                        independent_variables_list = final_independent_variables_list
                                                        )
        # Get Model Statistics
        statistics = getLinearRegressionModelStatistics(model = model, data_df = data_df, mean_vif = mean_vif)

        # Assign Statistics to all models row
        all_models_row['R2'] = statistics['rsquared']
        all_models_row['R2Adj'] = statistics['adjusted rsquared']
        all_models_row['DW'] = statistics['durbin watson']

        # Extract Model Summary table
        summary = model.summary()
        summary_table_html = summary.tables[1].as_html()
        summary_table_df = pd.read_html(summary_table_html, header=0, index_col=0)[0]
        summary_table_df.reset_index(inplace = True)

        # Add other start values to all models Row
        all_models_row = {
            'Dependent Variable' : dependent_variable_str,
            'Independent Variables' : [],
            'R2' : '',
            'R2Adj' : '',
            'DW' : '',
            'Sign OK' : 'OK',
            'ANOVA OK' : 'OK',
            'Colinealidad' : 'OK'
        }

        # Start worst sign dictionary to check which variable has the worst significancy so it can be taken out from the model
        worst_sign = {
            'variable' : '',
            'value' : ''
        }
        
        # Loop summary table to see if there is any non significant variable
        for index, row in summary_table_df.iterrows():
            # If the significancy value is over 0.05 and it is not an Obligatory Independent Variable or the Constant
            if (row['P>|t|'] > 0.05) and (row['index'] not in obligatory_independent_variables_list) and (row['index'] != 'const'):
                # Model Significancy is KO
                all_models_row['Sign OK'] = 'KO'
                # If we currently don't have any Variable stored as non-significant, store it
                if (worst_sign['value'] == ''):
                    worst_sign['value'] = str(row['P>|t|'])
                    worst_sign['variable'] = row['index']
                # If we have any Variable stored as non-significant, but this one's Significancy is worse, store it
                elif (worst_sign['value'] != '') and (row['P>|t|'] > float(worst_sign['value'])):
                    worst_sign['value'] = str(row['P>|t|'])
                    worst_sign['variable'] = row['index']
                else:
                    pass
            else:
                pass
        
        # Remove the model's worst non-significant variable from the Final Independent Variables List
        if all_models_row['Sign OK'] == 'KO':
            final_independent_variables_list.remove(worst_sign['variable'])
        else:
            pass
        
        # Add one to the model runs
        model_runs += 1

    # After all iterations the Best Independent Variables List is generated from the remaining Independent Variables
    best_independent_variables_list = final_independent_variables_list
    
    # Output is the list of the Best Independent Variables
    return best_independent_variables_list

def getAttributionData(data_df, dependent_variable_str, independent_variables_list, time_variable_str, model, languaje):
    ## Function to generate the Attribution Data Table
    # Inputs are the Data DataFrame, Dependent, Time and Independent Variables, Model and page's languaje

    # Start Attribution Data Columns list
    attribution_data_columns = []

    # Add to Attribution Data Columns the different columns needed: Time Variable, Constant and Independent Variables List
    attribution_data_columns.append(time_variable_str)
    attribution_data_columns.append('Constant')
    for variable in independent_variables_list:
        attribution_data_columns.append(variable)

    # Start Attribution Data DataFrame
    attribution_data_df = pd.DataFrame(columns = attribution_data_columns)

    # Set values for Time Variable Column
    attribution_data_df[time_variable_str] = data_df[time_variable_str]

    # Generate an auxiliary Independent Variables Table to predict for each variable one at a time to generate the attributed values
    aux_X = sm.add_constant(data_df[independent_variables_list])
    # Set al values to zero
    aux_X[:] = 0

    # Predict for each variable
    for variable in independent_variables_list:
        # Assing Variable values to auxiliary Table
        aux_X[variable] = data_df[variable]
        # Predict for variable
        prediction = model.predict(aux_X)
        # Assing predicted values to Attribution Data Table
        attribution_data_df[variable] = prediction
        # Restart Auxiliary table values for next variable
        aux_X[:] = 0

    # Assign constant values to Attribution Data Table
    attribution_data_df['Constant'] = model.params['const']

    # Rename Constant column if languaje is Spanish
    if languaje == 'SPA':
        attribution_data_df.rename(columns = {'Constant': 'Constante'}, inplace = True)
        
    # Output is the Attribution Data table
    return attribution_data_df

