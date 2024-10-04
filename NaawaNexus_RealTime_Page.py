import streamlit as st
import NaawaNexus_PageTop
import pages.NaawaNexus_Functions_RealTime as NaawaNexus_Functions_RealTime
from NaawaNexus_Menu import menu_with_redirect

# Pending parameters to find how to input them in the code
logoNaawa = 'www\\logo-naawa.png'
languaje = 'SPA'

st.set_page_config(page_title = 'NaawaNexus: Modelling' ,layout = 'wide')

def main():

    # Menu options
    menu = [':house: Home', ':microscope: Modelling', ':bulb: Real Time Model']

    # Page top
    st.header('Real Time')
    st.subheader(body = 'Keep learning ...')

    NaawaNexus_Functions_RealTime.Page_RealTime(languaje)
                
    # Redirect to app.py if not logged in, otherwise show the navigation menu
    menu_with_redirect()

if __name__ == '__main__':
    main()