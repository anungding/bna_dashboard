import streamlit as st
import altair as alt
from controllers.kesehatan_controller import KesehatanController

# Inisialisasi controller
kesehatan_controller = KesehatanController()

st.title("DATA KESEHATAN BNA 🚑🧑‍⚕️🦠")
st.subheader("DATA TENAGA KESEHATAN BNA 🧑‍⚕️")

# Ambil data yang telah digabungkan (cek apakah sudah ada di session state)
if 'df_combined' not in st.session_state:
    df_combined = kesehatan_controller.get_combined_data()
else:
    df_combined = st.session_state['df_combined']

# Filter untuk tahun dan kecamatan
years = df_combined['tahun'].unique()
kecamatans = df_combined['kecamatan'].unique()

# Pilih Tahun dan Kecamatan
col_sel_fil_1, col_sel_fil_2 = st.columns(2)
with col_sel_fil_1:
    selected_year = st.selectbox("Pilih Tahun", options=['Semua Tahun'] + list(years), index=0)
with col_sel_fil_2:
    selected_kecamatan = st.selectbox("Pilih Kecamatan", options=['Semua Kecamatan'] + list(kecamatans), index=0)

# Filter berdasarkan pilihan
filtered_data = kesehatan_controller.filter_data(df_combined, selected_year, selected_kecamatan)
total_dokter_2023 = kesehatan_controller.total_by_year(df_combined, 2023, 'dokter')
total_perawat_2023 = kesehatan_controller.total_by_year(df_combined, 2023, 'perawat')
total_bidan_2023 = kesehatan_controller.total_by_year(df_combined, 2023, 'bidan')


col_card_1, col_card_2, col_card_3 = st.columns(3)
with col_card_1:
    st.metric("Jumlah Dokter 2023", f"{total_dokter_2023}")
with col_card_2:
    st.metric("Jumlah Perawat 2023", f"{total_perawat_2023}")
with col_card_3:
    st.metric("Jumlah Bidan 2023", f"{total_bidan_2023}")
   
# Tampilkan tabel data yang sudah difilter
st.dataframe(filtered_data)
