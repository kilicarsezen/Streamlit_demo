import streamlit as st
from pages import page1, page2  # Import your page modules

from st_pages import Page, show_pages, add_page_title



def main():

    add_page_title("Welcome to the Inventory Controlling App", "🏠")
    # Specify what pages should be shown in the sidebar, and what their titles 
    # and icons should be
    show_pages(
        [
            Page("myapp/main.py", "Home", "🏡"),  # Changed icon
            Page("myapp/pages/page1.py", "Page 1", "📑"),  # Changed icon
            Page("myapp/pages/page2.py", "Inventory Data", "📊"),
        ]
    )
    
    
    st.write('''
        This app allows you to interact with inventory data, view details, add comments, and much more.
        Use the sidebar to navigate to different sections of the application:
        
        - **Page 1**: Inventory alert
        - **Page 2**: Explore and interact with inventory data.
        
        Select a page from the sidebar to get started.
        
    ''')
    # Embedding the dashboard URL into the link within the text
    st.markdown('Please visit our [Inventory Dashboard] to see the overall inventory figures.', unsafe_allow_html=True)



if __name__ == "__main__":
    main()
