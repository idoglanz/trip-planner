import streamlit as st
import pandas as pd


MEALS = ['Breakfast', 'Lunch', 'Dinner']


def update_ingredients_per_meal(columns, key):
     
    # update session state
    for indx, row in st.session_state[key]['edited_rows'].items():
        for col, val in row.items():
            st.session_state.per_meal_ingredients[key].loc[indx, col] = val

    for row in st.session_state[key]['added_rows']:
        new_row = {}
        for col in columns:
            if col in row:
                new_row[col] = row[col]
            else:
                new_row[col] = None
        st.session_state.per_meal_ingredients[key] = pd.concat([st.session_state.per_meal_ingredients[key], pd.DataFrame(new_row, index=[0])], ignore_index=True)



def meals(groceries_list):
    st.title("Whats to eat?")
    
    # ------ Where and Who inputs ------
    trip_days = pd.date_range(st.session_state.start_day, st.session_state.end_day, freq='D')

    # create tab for each day  
    tabs = st.tabs([day.strftime('🗓  %A, %d/%m') for day in trip_days])

    for indx, tab in enumerate(tabs):
        with tab:
            for meal in MEALS:
                title = f'{meal} for day {indx+1}'
                if title not in st.session_state.per_meal_ingredients:
                    st.session_state.per_meal_ingredients[title] = pd.DataFrame(columns=['name-price', 'quantity'])
                
                h_col, text_col = st.columns(2)
                h_col.subheader(title)
                _meal = text_col.text_input(label = title, label_visibility='collapsed', value=st.session_state.meals.get(title, ''))
                if _meal:
                    st.session_state.meals[title] = _meal
                with st.expander(f'{meal} Ingredients', expanded=False):
                    ingredients_element(groceries_list, key=title)



def ingredients_element(groceries_list, key):
    ingredients_df = st.session_state.per_meal_ingredients[key]
    st.data_editor(
        ingredients_df,
        column_config={
            "name-price": st.column_config.SelectboxColumn(
                "פריט",
                help='Select item from the list',
                width="large",
                options=groceries_list.df['name-price'].tolist(),
            ),
            "quantity": st.column_config.NumberColumn(
                "כמות",
                help="The quantity of the product",
                min_value=0,
                max_value=5000,
                step=0.1,
                format="%d",
            ),
        },
        hide_index=True,
        num_rows = 'dynamic',
        on_change=update_ingredients_per_meal,
        kwargs={'columns': ingredients_df.columns, 'key':key},
        key=key
    )
        
