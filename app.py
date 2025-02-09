import streamlit as st
from controllers.pendidikan_controller import PendidikanController
from controllers.disaster_controller import DisasterController
from controllers.pariwisata_controller import PariwisataController
from controllers.kesehatan_controller import KesehatanController

# Membuat halaman-halaman yang akan digunakan di dalam aplikasi Streamlit
beranda_page = st.Page("pages/beranda.py", title="Beranda", icon="⏹️")
bencana_page = st.Page("pages/disaster_view.py", title="Bencana", icon="🌋")
penduduk_page = st.Page("pages/penduduk.py", title="Penduduk", icon="👯")
pariwisata_page = st.Page("pages/pariwisata.py", title="Pariwisata", icon="🚠")
pendidikan_page = st.Page("pages/pendidikan.py", title="Pendidikan", icon="🎓")
kesehatan_page = st.Page("pages/kesehatan.py", title="Kesehatan", icon="🧑‍⚕️")
gis_page = st.Page("pages/gis.py", title="GIS", icon="🗺️")


if "pendidikan_controller" not in st.session_state:
    st.session_state["pendidikan_controller"] = PendidikanController() 
if "disaster_controller" not in st.session_state:
    st.session_state["disaster_controller"] = DisasterController() 
if "kesehatan_controller" not in st.session_state:
    st.session_state["kesehatan_controller"] = KesehatanController() 
if "pariwisata_controller" not in st.session_state:
    st.session_state["pariwisata_controller"] = PariwisataController()  

# Membuat navigasi halaman dengan icon dan judul masing-masing
pg = st.navigation(
    [
        beranda_page,  
        penduduk_page,  
        pariwisata_page,  
        pendidikan_page,  
        kesehatan_page, 
        bencana_page, 
        gis_page 
    ]
)

# Mengatur konfigurasi halaman Streamlit
st.set_page_config(page_title="BNA DASHBOARD", page_icon=":material/dashboard:", layout="wide")

# Menjalankan navigasi yang telah disiapkan
pg.run()
