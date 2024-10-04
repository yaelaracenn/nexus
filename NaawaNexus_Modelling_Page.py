import streamlit as st
import pandas as pd
from PIL import Image
import numpy as np
import plotly.express as px
from datetime import datetime
import NaawaNexus_PageTop
import pages.NaawaNexus_Functions_Modelling as NaawaNexus_Functions_Modelling
from NaawaNexus_Menu import menu_with_redirect

# Pending parameters to find how to input them in the code
logoNaawa = 'www\\logo-naawa.png'
logoCliente = 'www\\logo-cliente-hdi.png'
languaje = 'ENG'

st.set_page_config(page_title = 'NaawaNexus: Modelling' ,layout = 'wide')

def main():

    # Redirect to app.py if not logged in, otherwise show the navigation menu
    # menu_with_redirect()

    # Top Image
    # img = Image.open(logoNaawa)
    # st.image(img,use_column_width = False)
    img = Image.open(logoNaawa)
    imgcl = Image.open(logoCliente)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.image(img, width=200)

    with col2:
        st.write('')

    with col3:
        st.write('')
    
    with col4:
        st.image(imgcl, width=120)

    # # First expander - Modelling
    # with st.expander(label = menu[1], expanded = False):
    NaawaNexus_Functions_Modelling.Page_Modelling(languaje)
                
    # # Second expander - Real Time
    # with st.expander(label = menu[2], expanded = False):
    #     NaawaNexus_Page_Realtime.Page_RealTime()
    #     modelExpanded = True
    menu_with_redirect()
        
if __name__ == '__main__':
    main()