import streamlit as st
import altair as alt
from controllers.kesehatan_controller import KesehatanController

# Inisialisasi controller
kesehatan_controller = KesehatanController()

st.title("DATA KESEHATAN BNA")

# ---------------- TENAGA KESEHATAN ----------------
st.markdown(
    """
    ### 🧑‍⚕️DATA TENAGA KESEHATAN BNA🧑‍⚕️
    Dataset diambil dari: -
    
    Periode: 2018-2023
    """
)

# Ambil data yang telah digabungkan
df_combined = kesehatan_controller.get_combined_data()

# Filter untuk tahun dan kecamatan
years = df_combined['tahun'].unique()
kecamatans = df_combined['kecamatan'].unique()

# Pilih Tahun dan Kecamatan
selected_year = st.selectbox("Pilih Tahun", options=['Semua Tahun'] + list(years), index=0)
selected_kecamatan = st.selectbox("Pilih Kecamatan", options=['Semua Kecamatan'] + list(kecamatans), index=0)

# Filter berdasarkan pilihan
filtered_data = kesehatan_controller.filter_data(df_combined, selected_year, selected_kecamatan)

# Tampilkan tabel data yang sudah difilter
st.dataframe(filtered_data)
