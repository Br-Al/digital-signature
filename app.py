import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageEnhance
from streamlit_cropper import st_cropper
from datetime import datetime

aitecaf_logo = Image.open('./assets/imgs/AITECAF-black.png')
title_container, logo_container = st.columns([0.8, 0.2])
with title_container:
    st.markdown("""<style> .title { font-family: 'Nexa'; color: #008037; } body {background-color: white;}</style>""", unsafe_allow_html=True)
    st.markdown('<h1 class="title"> Digitalize Your signature </h1>', unsafe_allow_html=True)
with logo_container:
    st.image(aitecaf_logo)


def digitalize(uploaded_signature):
    signature = Image.open(uploaded_signature)
    
    cropped = st_cropper(signature, aspect_ratio=(16, 9))
    converted_signature = np.array(cropped.convert('RGB'))
    sign_gray = cv2.cvtColor(converted_signature, cv2.COLOR_BGR2GRAY)
    _, alpha_mask = cv2.threshold(sign_gray, threshold, 255, cv2.THRESH_BINARY_INV)
    color_mask = converted_signature.copy()
    color_mask[:, :] = rgb_color
    sign_color = cv2.addWeighted(converted_signature, 1, color_mask, 0.5, 0)
    b, g, r = cv2.split(sign_color)
    new = [b, g, r, alpha_mask]
    png = cv2.merge(new, 4)
    return png

def save(img):
    file_name = f'signed-{datetime.now().strftime("%d%m%y%H%M%S")}.png'
    cv2.imwrite(f'./assets/imgs/signatures/{file_name}', img)
    with open(f'./assets/imgs/signatures/{file_name}', 'rb') as file:
        btn = st.download_button('Download', file, file_name='signed.png', mime='image/png')

#### Sidebar

with st.sidebar:
    st.image(aitecaf_logo)
    st.write("""This is a Digital Signature Using OpenCV""")
    st.write("By Kenfack Anafack Alex Bruno: [LinkedIn](https://www.linkedin.com/in/bruno-alex-kenfack-anafack-5a82b4151/)")

with st.sidebar.expander("About this App"):  
    st.write("""Use this simple app to digitalize your signatire. Download and paste it in any digital document.""")
    st.write("""This app was created By [Kenfack Anafack Alex Bruno](https://www.linkedin.com/in/bruno-alex-kenfack-anafack-5a82b4151/)
    as a side project to learn streamlit and Computer vision. Hope you enjoy!""")

with st.sidebar:
    hexa_color = st.color_picker('color').lstrip('#')
    rgb_color = tuple(int(hexa_color[i:i+2], 16) for i in (0, 2, 4))
    threshold = st.slider("Threahold", min_value=0, max_value=255, value=150, step=1)

upload_option = st.radio('', ('Upload from galery', 'Take a picture'), horizontal=True)
if upload_option == "Upload from galery":
    uploaded_signature = st.file_uploader('Uploads a picture of your signature', type=['png', 'jpg', 'jpeg'])
else:
    uploaded_signature = st.camera_input('Take a picture of your signature')
original, output = st.columns(2)
saved = False
if uploaded_signature is not None:
    digital_signature = digitalize(uploaded_signature)
    st.image(digital_signature)
    save_column, download_column = st.columns(2)
    with save_column:
        if st.button('Save'):
            file_name = f'signed-{datetime.now().strftime("%d%m%y%H%M%S")}.png'
            cv2.imwrite(f'./assets/imgs/signatures/{file_name}', digital_signature)
            saved = True
    if saved:        
        with open(f'./assets/imgs/signatures/{file_name}', 'rb') as file:
            with download_column:
                btn = st.download_button('Download', file, file_name='signed.png', mime='image/png')

