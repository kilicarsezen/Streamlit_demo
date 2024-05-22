# In pages/page2.py

import streamlit as st
from myapp.database.operations import get_high_inventory_materials


def process_uploaded_inventory_file(file, filename):
    pass



if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def set_clicked():
    st.session_state.clicked = True 

def submit_excel_file():
    st.title('Upload Inventory Files')
    st.markdown("---")
    st.button('Upload File', on_click=set_clicked)
    if st.session_state.clicked:
        uploaded_file = st.file_uploader("Plese upload an excel sheet", type='xlsx')
        if uploaded_file is not None:
            filename=uploaded_file.name
            process_uploaded_inventory_file(uploaded_file, filename)
        else:
            st.warning("you need to upload a csv or excel file.")

def app():    
    submit_excel_file()

    st.title('Inventory Level Alert')

    # Allow the user to set the threshold
    threshold = st.number_input('Set the inventory threshold', value=100)  # Default value is 100

    if st.button('Check Inventory'):
        high_inventory_items = get_high_inventory_materials(threshold)

        if high_inventory_items:
            st.warning(f"Materials exceeding the inventory threshold of {threshold}:")
            for item in high_inventory_items:
                st.write(f"Code Number: {item.code_number}, Description: {item.description}, Total Quantity: {item.total_quantity}")
        else:
            st.success("No materials exceed the inventory threshold.")

if __name__ == "__main__":
    app()
