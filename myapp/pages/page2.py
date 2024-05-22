import pandas as pd
import streamlit as st
from myapp.database.operations import fetch_inventory_data, get_existing_comment, save_comment, get_inventory_distribution
from datetime import datetime

def create_inventory_pivot_table(data):
    # Convert list of data to DataFrame
    df = pd.DataFrame(data, columns=['Date', 'Material', 'Quantity'])
    
    # Format the 'Date' column to date-only strings
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
    
    # Pivot the data to get dates as columns and materials as rows
    pivot_df = df.pivot_table(values='Quantity', index='Material', columns='Date', aggfunc='sum', fill_value=0)
    
    return pivot_df



def show_inventory_table():
    data = fetch_inventory_data()
    pivot_df = create_inventory_pivot_table(data)

    st.write(pivot_df)

    material_selected = st.selectbox('Select Material', pivot_df.index.tolist())

    # Convert datetime objects or strings with time data to date-only strings for the dropdown
    dates = [date.strftime('%Y-%m-%d') if isinstance(date, pd.Timestamp) else date.split(' ')[0] for date in pivot_df.columns.tolist()]
    date_selected = st.selectbox('Select Date', dates)

    # Fetch the existing comment for the selected material and date
    existing_comment = get_existing_comment(material_selected, date_selected)

    if existing_comment:
        st.write(f"Current Comment: {existing_comment.comment}")
        if st.button('Edit Comment'):
            st.session_state['edit_mode'] = True
    else:
        st.write("No existing comment.")
        st.session_state['edit_mode'] = True  # Allow to add a new comment

    if st.session_state.get('edit_mode', False):
        # If in edit mode, show text area with existing comment or empty for new comment
        new_comment = st.text_area("Comment", value=existing_comment.comment if existing_comment else '')
        if st.button('Save Comment'):
            # Save logic should correctly associate the comment with the material, date, and specific InventoryHistory record
            result_message = save_comment(material_selected, date_selected, new_comment, existing_comment.id if existing_comment else None)
            st.session_state['edit_mode'] = False  # Exit edit mode after saving

    # Inventory distribution visualization
    st.write("Inventory Distribution by Location and Date")

    if len(dates) > 1:
        start_date, end_date = st.select_slider(
            "Select date range",
            options=dates,
            value=(dates[0], dates[-1])
        )
    else:
        # Only one date available
        st.write(f"Only one date available: {dates[0]}")
        start_date, end_date = dates[0], dates[0]

    start_date_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_dt = datetime.strptime(end_date, '%Y-%m-%d')
    distribution_data = get_inventory_distribution(material_selected, start_date_dt, end_date_dt)
    if distribution_data:
        df_distribution = pd.DataFrame(distribution_data)
        st.bar_chart(df_distribution.pivot(index='date', columns='location', values='total_quantity'))
    else:
        st.write('No inventory distribution data available for the selected material and date range.')

def app():
    st.title('Inventory Data')
    show_inventory_table()  # Assuming this is the function that handles your inventory table and comments.

if __name__ == "__main__":
    app()