import streamlit as st
import pandas as pd


def update_equipment(columns):
     
    # update session state
    for indx, row in st.session_state['equipment_list']['edited_rows'].items():
        for col, val in row.items():
            st.session_state.equipment.loc[indx, col] = val
    
    for row in st.session_state['equipment_list']['added_rows']:
        new_row = {}
        for col in columns:
            if col in row:
                new_row[col] = row[col]
            else:
                new_row[col] = None
        
        st.session_state.equipment = pd.concat([st.session_state.equipment, pd.DataFrame(new_row, index=[0])], ignore_index=True)



def equipment_list():
    st.title("Equipment List")

    equipment = st.session_state.equipment

    st.data_editor(equipment,
                    num_rows = 'dynamic', 
                    key='equipment_list', 
                    on_change=update_equipment,
                    hide_index=True,
                    kwargs={'columns': equipment.columns},
                    width=1400,
                    )
    


    @st.cache_data
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')


    csv = convert_df(equipment)

    st.download_button(
        "Press to Download",
        csv,
        "equipment_list.csv",
        "text/csv",
        key='download-csv'
        )