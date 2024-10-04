import streamlit as st
from PIL import Image

def NaawaNexus_PageTop(logoNaawa,logoCliente, menu, language_str):
    # Top Image
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

    if language_str == 'ENG':
        # Page title
        st.title(body = 'Welcome to DemandAI')
        st.write('In this app, you will be able to create and analyze business demand models to gain valuable insights into your marketing strategies. Additionally, you will harness the power of machine learning to make accurate forecasts and optimize your business decisions.')
        # Instructions
        st.header(body = 'Instructions')
        st.write('1. ' + menu[1] + ': Conect your data and create your own business demand models. Find out which is the best possible fit for your dataset')
        st.write('2. ' + menu[2] + ': Analyze attribution and the ROI of your efforts.')
        st.write('3. ' + menu[3] + ': Create scenarios and analyze the incremental demand of future efforts.')
        st.write('4. ' + menu[4] + ': Keep learning...')
        
    elif language_str == 'SPA':
        # Page title
        st.title(body = 'Bienvenid@ a NaawaNexus')
        st.write('En esta app serás capaz de...')
        # Instructions
        st.header(body = 'Instrucciones')
        st.write('1. Modelling: En la pestaña ' + menu[1] + ' podrás correr Modelos de Regresión Lineal para encontrar los drivers que impactan la Demanda Incremental de tu negocio, un resumen del modelo generado, una visualización del modelo y la realidad, y la composición del modelo para estudiar el peso de cada driver sobre la Demanda Incremental de tu negocio.')
        st.write('2. En vivo: En la pestaña ' + menu[2] + ' podrás ver la evolución de tu modelo en vivo.')
    else:
        st.error('Languaje not supported')