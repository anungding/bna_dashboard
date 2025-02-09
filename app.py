import streamlit as st
from controllers.pendidikan_controller import PendidikanController
from controllers.disaster_controller import DisasterController
from controllers.tourism_controller import TourismController
from controllers.kesehatan_controller import KesehatanController

home_page = st.Page("pages/home_view.py", title="Beranda", icon="⏹️")
disaster_page = st.Page("pages/disaster_view.py", title="Bencana", icon="🌋")
penduduk_page = st.Page("pages/penduduk.py", title="Penduduk", icon="👯")
tourism_page = st.Page("pages/tourism_view.py", title="Pariwisata", icon="🚠")
pendidikan_page = st.Page("pages/pendidikan.py", title="Pendidikan", icon="🎓")
kesehatan_page = st.Page("pages/kesehatan.py", title="Kesehatan", icon="🧑‍⚕️")
gis_page = st.Page("pages/gis.py", title="GIS", icon="🗺️")


if "pendidikan_controller" not in st.session_state:
    st.session_state["pendidikan_controller"] = PendidikanController() 
if "disaster_controller" not in st.session_state:
    st.session_state["disaster_controller"] = DisasterController() 
if "kesehatan_controller" not in st.session_state:
    st.session_state["kesehatan_controller"] = KesehatanController() 
if "tourism_controller" not in st.session_state:
    st.session_state["tourism_controller"] = TourismController()  

pg = st.navigation(
    [
        home_page, 
        penduduk_page,  
        tourism_page,  
        pendidikan_page,  
        kesehatan_page, 
        disaster_page, 
        gis_page 
    ]
)

st.set_page_config(page_title="BNA DASHBOARD", page_icon=":material/dashboard:", layout="wide")

pg.run()
