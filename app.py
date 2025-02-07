import streamlit as st



beranda_page = st.Page("pages/beranda.py", title="Beranda", icon="⏹️")
bencana_page = st.Page("pages/bencana.py", title="Bencana", icon="🌋")
penduduk_page = st.Page("pages/penduduk.py", title="Penduduk", icon="👯")
pariwisata_page = st.Page("pages/pariwisata.py", title="Pariwisata", icon="🚠")
pendidikan_page = st.Page("pages/pendidikan.py", title="Pendidikan", icon="🎓")
kesehatan_page = st.Page("pages/kesehatan.py", title="Kesehatan", icon="🧑‍⚕️")
gis_page = st.Page("pages/gis.py", title="GIS", icon="🗺️")


# Pastikan controller sudah ada di session_state
from controllers.pendidikan_controller import PendidikanController

if "pendidikan_controller" not in st.session_state:
    st.session_state["pendidikan_controller"] = PendidikanController()


pg = st.navigation(
    [
        beranda_page, 
        bencana_page, 
        penduduk_page, 
        pariwisata_page, 
        pendidikan_page,
        kesehatan_page,
        gis_page
    ]
)
st.set_page_config(page_title="BNA DASHBOARD", page_icon=":material/dashboard:", layout="wide")
pg.run()


