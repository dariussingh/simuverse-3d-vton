import streamlit as st
import os
from PIL import Image

st.set_page_config(layout='wide')

st.title('SimuVerse 3D Virtual Try-on App')
st.write('This app enables virtual try-on given input images of a clothing item and person.')

st.header('Input')

col1, col2 = st.columns((1,1))

col1.subheader('Clothing')
col2.subheader('Person')
clothing = col1.file_uploader('Upload Cloth Image', type=['jpg', 'png', 'jpeg'])
person = col2.file_uploader('Upload Person Image', type=['jpg', 'png', 'jpeg'])

if st.button('Run Virtual Try-On'):
    if (clothing is None) or (person is None):
        st.write('**Error**: input images not provided!')
    else:
        st.header('Output')

        
