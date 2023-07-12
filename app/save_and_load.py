import os
import pandas as pd
import streamlit as st


"""
Trip File and Info
    trip_name - str
    attendees - df
    start_day - datetime
    end_day - datetime
    meals - dict
    per_meal_ingredients - dict{meal: df}
    equipment - df

"""

def save_trip_files(path):
    """Saves all trip files to xlsx file"""
    filename = st.session_state.trip_name.replace(' ','-') + st.session_state.start_day.strftime('_%d-%m-%Y') + '_to_' + st.session_state.end_day.strftime('%d-%m-%Y') + '.xlsx'
    with pd.ExcelWriter(os.path.join(path,filename)) as writer:  # doctest: +SKIP
        st.session_state.attendees.to_excel(writer, sheet_name='attendees')
        if 'equipment' in st.session_state:
            st.session_state.equipment.to_excel(writer, sheet_name='equipment')
        for meal, ingredients in st.session_state.per_meal_ingredients.items():
            if ingredients.empty:
                continue
            ingredients.to_excel(writer, sheet_name=meal)


def load_trip_files(filename):
    """Loads all trip files from xlsx file"""
    # extract trip name, start and end dates from filename
    # Summer-2023_12-07-2023_to_14-07-2023.xlsx
    filename_parts = filename.name.split('.')[0].split('_')
    st.session_state.trip_name = filename_parts[0]
    st.session_state.start_day = pd.to_datetime(filename_parts[1], format='%d-%m-%Y')
    st.session_state.end_day = pd.to_datetime(filename_parts[3], format='%d-%m-%Y')
    print(filename)
    with pd.ExcelFile(filename) as reader:
        st.session_state.attendees = pd.read_excel(reader, sheet_name='attendees')
        if 'equipment' in reader.sheet_names:
            st.session_state.equipment = pd.read_excel(reader, sheet_name='equipment')
        for meal in reader.sheet_names:
            if meal == 'attendees' or meal == 'equipment':
                continue
            st.session_state.per_meal_ingredients[meal] = pd.read_excel(reader, sheet_name=meal)