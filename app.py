import streamlit as st
from components.sidebar.sidebar import initialize_controllers, create_sidebar

# Set up page configuration
st.set_page_config(page_title="BNA DASHBOARD", page_icon=":material/dashboard:", layout="wide")

# Initialize controllers
initialize_controllers()

# Create sidebar and run navigation
pg = create_sidebar()
pg.run()
