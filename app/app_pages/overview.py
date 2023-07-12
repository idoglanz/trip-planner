import streamlit as st
import pandas as pd


def update_attendees(columns):
     
    # update session state
    for indx, row in st.session_state['attendees_list']['edited_rows'].items():
        for col, val in row.items():
            st.session_state.attendees.loc[indx, col] = val
    
    for row in st.session_state['attendees_list']['added_rows']:
        new_row = {}
        for col in columns:
            if col in row:
                new_row[col] = row[col]
            else:
                new_row[col] = 0 if col != 'name' else 'New Attendee'
        
        st.session_state.attendees = pd.concat([st.session_state.attendees, pd.DataFrame(new_row, index=[0])], ignore_index=True)


def overview(attendees):

    st.title("Yalla Lets Plan")

    # ----- Days input -----

    st.subheader('When are we going?')
    start, end = st.columns(2)
    start_day = start.date_input('Start Date', value=st.session_state.start_day)
    end_day = end.date_input('End Date', value= st.session_state.end_day)

    if start_day > end_day:
        st.error('Sorry! End date must fall after start date.')
    if start_day != st.session_state.start_day:
        st.session_state.start_day = start_day
    if end_day != st.session_state.end_day:
        st.session_state.end_day = end_day
    
    st.write(f'Total Nights: {(end_day - start_day).days}')
    
    who_col, where_col = st.columns(2)
    trip_days = pd.date_range(start_day, end_day, freq='D')

    # ------ Where and Who inputs ------

    # drop columns not in trip_days
    for col in attendees.columns:
        if col not in trip_days.strftime('%A, %d/%m').tolist() and col != 'name':
            attendees.drop(col, axis=1, inplace=True)

    # add columns for trip days
    for day in trip_days:
        if day.strftime('%A, %d/%m') not in attendees.columns:
            attendees[day.strftime('%A, %d/%m')] = [0 for i in range(len(attendees))]
            
    
    with who_col:
        st.subheader("Who's coming?")
        # add column for each day
        st.data_editor(attendees,
                    num_rows = 'dynamic', 
                    key='attendees_list', 
                    on_change=update_attendees, 
                    hide_index=True,
                    kwargs={'columns': attendees.columns},
                    width=800,
                    )

        st.write('Total Attendees:')
        totals_df = attendees.copy()
        totals_df.drop('name', axis=1, inplace=True)

        print(totals_df)
        totals_df = totals_df.sum(axis=0).to_frame().T
        st.dataframe(totals_df, width=800, hide_index=True)

    coords = {'lat': 33.15910793777419,'lon': 35.61595799494331}
    coords_df = pd.DataFrame(coords, index=[0])
    where_col.map(coords_df, zoom=10)
