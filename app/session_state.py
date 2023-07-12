import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

EQUIPMENT_COLUMNS = ['ציוד', 'כמות', 'אחריות', 'הערות']


def init_state_session_vars():

    if 'trip_name' not in st.session_state:
        st.session_state.trip_name = 'Summer 2023'

    if 'attendees' not in st.session_state:
        st.session_state.attendees = pd.DataFrame(columns=['name'])

    if 'start_day' not in st.session_state:
        st.session_state.start_day = datetime.now()

    if 'end_day' not in st.session_state:
        st.session_state.end_day = datetime.now() + timedelta(days=2)

    if 'meals' not in st.session_state:
        st.session_state.meals = {}

    if 'per_meal_ingredients' not in st.session_state:
        st.session_state.per_meal_ingredients = {}

    if 'equipment' not in st.session_state:
        st.session_state.equipment = pd.DataFrame(columns=EQUIPMENT_COLUMNS)
    