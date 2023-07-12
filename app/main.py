from st_on_hover_tabs import on_hover_tabs
import streamlit as st
from PIL import Image
import pandas as pd
from datetime import datetime, timedelta

from app.signin import check_password
from app.app_pages.overview import overview
from app.app_pages.meals import meals
from app.app_pages.shopping_list import shopping_list
from app.xml_parser import parse_xml
from app.app_pages.equipment import equipment_list
from app.fetch_prices import get_price_list_filename
from app.save_and_load import save_trip_files, load_trip_files
from app.session_state import init_state_session_vars

im = Image.open('./data/assets/tripping_logo_1.png')
st.set_page_config(page_title="Tripping", page_icon=im, layout='wide')


hide_default_format = """
       <style>
       .css-k1ih3n {padding: 2rem 1rem 10rem;}
       .css-1n3k81r {min-width: 100px;}
       .css-1vq4p4l {padding: 3rem 1rem 1.5rem}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)


@st.cache_data
def load_shopping_list():
    filename = get_price_list_filename()
    groceries_list = parse_xml(filename)
    return groceries_list

groceries_list = load_shopping_list()

st.header("Camping Planning App 2023 (v0.1)")
st.markdown('<style>' + open('./app/style.css').read() + '</style>', unsafe_allow_html=True)

init_state_session_vars()

with st.sidebar:
    st.image('./data/assets/tripping_logo_1.png',use_column_width=True, width=100)
    st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)    # add spacing

        
    trip_name = st.text_input(label = 'Trip Name', label_visibility='collapsed', value=st.session_state.trip_name)
    if trip_name:
        st.session_state.trip_name = trip_name
    
    tabs = on_hover_tabs(tabName=['Overview', 'Meals', 'Shopping List', 'Equipment List'], 
                         iconName=['forest','restaurant', 'shopping_cart', 'construction'], default_choice=0)

    if st.button('Save', use_container_width=True):
        save_trip_files('./data/trips')
    load_file = st.file_uploader('Load', type=['xlsx'])
    if load_file:
        load_trip_files(load_file)



if tabs =='Overview' and check_password():
    overview(st.session_state.attendees)

elif tabs == 'Meals' and check_password():
    meals(groceries_list)

elif tabs == 'Shopping List' and check_password():
    shopping_list(groceries_list)

elif tabs == 'Equipment List' and check_password():
    equipment_list()
