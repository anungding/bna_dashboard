import streamlit as st
from controllers.education_controller import EducationController
from controllers.disaster_controller import DisasterController
from controllers.tourism_controller import TourismController
from controllers.healty_controller import HealtyController

def initialize_controllers():
    """Menyimpan controller ke dalam session state jika belum ada."""
    if "education_controller" not in st.session_state:
        st.session_state["education_controller"] = EducationController()
    if "disaster_controller" not in st.session_state:
        st.session_state["disaster_controller"] = DisasterController()
    if "healty_controller" not in st.session_state:
        st.session_state["healty_controller"] = HealtyController()
    if "tourism_controller" not in st.session_state:
        st.session_state["tourism_controller"] = TourismController()

def create_sidebar():
    """Membuat sidebar dan navigasi antar halaman."""
    home_page = st.Page("pages/home_view.py", title="Beranda", icon="⏹️")
    disaster_page = st.Page("pages/disaster_view.py", title="Bencana", icon="🌋")
    penduduk_page = st.Page("pages/penduduk.py", title="Penduduk", icon="👯")
    tourism_page = st.Page("pages/tourism_view.py", title="Pariwisata", icon="🚠")
    education_page = st.Page("pages/education_view.py", title="Pendidikan", icon="🎓")
    healty_page = st.Page("pages/healty_view.py", title="Kesehatan", icon="🧑‍⚕️")
    gis_page = st.Page("pages/gis.py", title="GIS", icon="🗺️")

    pg = st.navigation(
        [
            home_page, 
            penduduk_page,  
            tourism_page,  
            education_page,  
            healty_page, 
            disaster_page, 
            gis_page 
        ]
    )
    return pg
