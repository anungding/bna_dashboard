import streamlit as st
from controllers.pendidikan_controller import PendidikanController
from controllers.bencana_controller import BencanaController
from controllers.pariwisata_controller import PariwisataController

# Membuat halaman-halaman yang akan digunakan di dalam aplikasi Streamlit
beranda_page = st.Page("pages/beranda.py", title="Beranda", icon="⏹️")
bencana_page = st.Page("pages/bencana.py", title="Bencana", icon="🌋")
penduduk_page = st.Page("pages/penduduk.py", title="Penduduk", icon="👯")
pariwisata_page = st.Page("pages/pariwisata.py", title="Pariwisata", icon="🚠")
pendidikan_page = st.Page("pages/pendidikan.py", title="Pendidikan", icon="🎓")
kesehatan_page = st.Page("pages/kesehatan.py", title="Kesehatan", icon="🧑‍⚕️")
gis_page = st.Page("pages/gis.py", title="GIS", icon="🗺️")


if "pendidikan_controller" not in st.session_state:
    st.session_state["pendidikan_controller"] = PendidikanController() 
if "bencana_controller" not in st.session_state:
    st.session_state["bencana_controller"] = BencanaController() 
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
