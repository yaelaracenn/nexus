import streamlit as st
import NaawaNexus_PageTop
import NaawaNexus_Menu

# Pending parameters to find how to input them in the code
logoNaawa = 'www\\logo-naawa.png'
logoCliente = 'www\\logo-cliente-hdi.png'
languaje = 'ENG'


st.set_page_config(page_title = 'NaawaNexus' ,layout = 'wide')

def main(): 
    # Menu options
    menu = [':house: Home', ':microscope: Modelling', ':bar_chart: Outcome', ':chart_with_upwards_trend: Forecast', ':bulb: Real Time Model']
    actions = ['Home', 'Modelling', 'Outcome', 'Real Time Model']

    # Page top
    NaawaNexus_PageTop.NaawaNexus_PageTop(logoNaawa, logoCliente, menu, languaje)
    initialise()
    retrieve_session_state()
    NaawaNexus_Menu.menu()

def initialise():
    # Initialize st.session_state.role to None
    if "action" not in st.session_state:
        st.session_state.action = None

    if 'model' not in st.session_state:
        st.session_state.model = None

    if 'input_data_file' not in st.session_state:
        st.session_state.input_data_file = None

    if 'time_variable_str' not in st.session_state:
        st.session_state.time_variable_str = None

    if 'modelVsReal' not in st.session_state:
        st.session_state.modelVsReal = None

    if 'independent_variables_list' not in st.session_state:
        st.session_state.independent_variables_list = None

    if 'dependent_variable_str' not in st.session_state:
        st.session_state.dependent_variable_str = None

def retrieve_session_state():
    # Retrieve the role from Session State to initialize the widget
    st.session_state._action = st.session_state.action
    st.session_state._model = st.session_state.model
    st.session_state._input_data_file = st.session_state.input_data_file
    st.session_state._time_variable_str = st.session_state.time_variable_str
    st.session_state._modelVsReal = st.session_state.modelVsReal
    st.session_state._independent_variables_list = st.session_state.independent_variables_list
    st.session_state._dependent_variable_str = st.session_state.dependent_variable_str


def set_action():
    # Callback function to save the role selection to Session State
    st.session_state.action = st.session_state._action
        
if __name__ == '__main__':
    main()