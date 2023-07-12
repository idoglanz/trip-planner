import streamlit as st
import pandas as pd


def construct_shopping_list_from_meals(meals, groceries_list):
    shopping_list = {}
    for _, ingredients in meals.items():
        for _, row in ingredients.iterrows():
            uuid = groceries_list.get_uuid_from_name_price(row['name-price'])

            if uuid not in shopping_list:
                item_row = groceries_list.get_row_by_uuid(uuid).copy()
                item_row['quantity'] = row['quantity']
                item_row['price']  = float(item_row['price'])*row['quantity']
                shopping_list[uuid] = item_row

            else:
                item_row = groceries_list.get_row_by_uuid(uuid).copy()
                shopping_list[uuid]['quantity'] += row['quantity']
                shopping_list[uuid]['price'] = float(item_row['price'])*row['quantity']

    return shopping_list


def shopping_list(groceries_list):
    st.title("Food Shopping List")

    st.subheader('Shopping List for meals')

    if 'all_ingredients' not in st.session_state:
        st.session_state.all_ingredients = pd.DataFrame(columns=['name', 'quantity', 'uuid'])

    if 'per_meal_ingredients' in st.session_state and st.session_state.per_meal_ingredients != {}:
        meals_shopping_list_dict = construct_shopping_list_from_meals(st.session_state.per_meal_ingredients, groceries_list)
        meals_shopping_list = pd.DataFrame.from_dict(meals_shopping_list_dict, orient='index')
        
        st.dataframe(meals_shopping_list,
                    column_order=['name', 'quantity', 'units', 'price'], 
                    width=1400, 
                    # height=600,
                    hide_index=True,
                    column_config={
                        "price": st.column_config.NumberColumn(
                            "סה״כ מחיר בש״ח",
                            help="The price of the product in ILS",
                            min_value=0,
                            max_value=5000,
                            step=0.1,
                            format="%f₪",
                        ),
                        "quantity": st.column_config.NumberColumn( 
                            "כמות",
                            help="The quantity of the product",
                            min_value=0,
                            max_value=5000,
                            step=0.1,
                            format="%d",
                        ),
                        "units": st.column_config.TextColumn(
                            "יחידות",
                            help="The units of the product",
                            width="100px",
                        ),
                        "name": st.column_config.TextColumn(
                            "פריט",
                            help="The name of the product",
                            width="100px",
                        )
                })
    

    st.subheader('Get Price By Name')
    st.selectbox('Select Item', groceries_list.df['name-price'].tolist())

    st.title("Available Items")
    st.dataframe(groceries_list.df, 
                 width=1400, 
                 height=600, 
                 hide_index=True,
                 column_config={
                    "price": st.column_config.NumberColumn(
                    "מחיר בש״ח",
                    help="The price of the product in ILS",
                    min_value=0,
                    max_value=5000,
                    step=0.1,
                    format="%d.2₪",
                    )
                },)
