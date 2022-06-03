import streamlit as st
import base64
import cv2
from beerscanfrontend.utils import rectangle, boxes_request
import numpy as np


st.set_page_config(
            page_title="BeerScan", # => Quick reference - Streamlit
            page_icon="🍻",
            layout="centered", # wide
            initial_sidebar_state="auto") # collapsed


hide_menu_style = """
        <style>
        .css-hy8qiv {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


local_css("style.css")



@st.cache
def load_image(path):
    with open(path, 'rb') as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    return encoded

def image_tag(path):
    encoded = load_image(path)
    tag = f'<img src="data:image/png;base64,{encoded}">'
    return tag

def background_image_style(path):
    encoded = load_image(path)
    style = f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
    }}
    </style>
    '''
    return style

image_path = 'images/background2.png'

st.write(background_image_style(image_path), unsafe_allow_html=True)
with st.container():
    st.markdown("<h1 style=' text-shadow: 2px 2px #ff0000;font-family: Helvetica ;text-align: center;font-size:100px; color: #F08080;'>BeerScan</h1>", unsafe_allow_html=True)
    st.markdown(" ")
    st.markdown(" ")
    st.markdown("<p style=' text-shadow: 2px 2px #ffffff;font-family: Helvetica ;text-align: center;font-size:50px; color: black ;'>Press here</p>", unsafe_allow_html=True)


with st.expander(" "):
    uploaded_file = st.file_uploader("png or jpg",type=["png","jpg","JPEG","WEBP"])
    if uploaded_file is not None:
        with st.spinner('Wait for it...'):
            #converting the upload to a np_array
            bytes_res = uploaded_file.getvalue()
            nparr = np.fromstring(bytes_res, np.uint8)

            #converting nparray back to a image for the rectangle fcts
            img_np = cv2.cvtColor(cv2.imdecode(nparr, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)

            #calling the api through a boxes fonction to find the bottles
            boxes = boxes_request(bytes_res)

            #case of no bottles
            if not bool(boxes):
                st.markdown("No bottle found in this picture, please try another one")
            #Making the new image with the rectangles
            st.image(rectangle(cv2.cvtColor(cv2.imdecode(nparr, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB),boxes))
