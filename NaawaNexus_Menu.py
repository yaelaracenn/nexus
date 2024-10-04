import streamlit as st
from PIL import Image

actions = ['Home', 'Modelling', 'Outcome', 'Forecast', 'Real Time']
# logo = 'www\\naawa-logo.png'

def authenticated_menu():
    # img2 = Image.open(logo)
    # st.sidebar.image(img2,use_column_width = True)
    # Show a navigation menu for authenticated users
    st.sidebar.page_link('NaawaNexus2.py', label = actions[0])
    st.sidebar.page_link('pages/NaawaNexus_Modelling_Page.py', label = actions[1])

    if st.session_state.model is not None:
        st.sidebar.page_link('pages/NaawaNexus_Outcome_Page.py', label = actions[2])
        st.sidebar.page_link('pages/NaawaNexus_Forecast_Page.py', label = actions[3])
        st.sidebar.page_link('pages/NaawaNexus_RealTime_Page.py', label = actions[4])
    else:
        st.sidebar.page_link(
            'pages/NaawaNexus_Outcome_Page.py',
            label = actions[2],
            disabled = st.session_state.action != actions[2]
        )
        st.sidebar.page_link(
            'pages/NaawaNexus_Forecast_Page.py',
            label = actions[3],
            disabled = st.session_state.action != actions[3]
        )
        st.sidebar.page_link(
            'pages/NaawaNexus_RealTime_Page.py',
            label = actions[4],
            disabled = st.session_state.action != actions[4]
        )

def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    #st.sidebar.page_link("NaawaNexus2.py", label=actions[0])
    authenticated_menu()

def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    # if "action" not in st.session_state or st.session_state.action is None:
    #     unauthenticated_menu()
    #     return
    authenticated_menu()

def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    # if "action" not in st.session_state or st.session_state.action is None:
    #     st.switch_page("NaawaNexus2.py")
    menu()
