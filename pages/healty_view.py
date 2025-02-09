import streamlit as st
import altair as alt
from controllers.healty_controller import HealtyController

# Inisialisasi controller
healty_controller = HealtyController()

st.title("DATA KESEHATAN BNA 🚑🧑‍⚕️🦠")
st.markdown("""
---
""")
st.subheader("DATA TENAGA KESEHATAN BNA 🧑‍⚕️")

# Ambil data yang telah digabungkan (cek apakah sudah ada di session state)
if 'df_combined' not in st.session_state:
    df_combined = healty_controller.get_combined_data()
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
filtered_data = healty_controller.filter_data(df_combined, selected_year, selected_kecamatan)

col_card_1, col_card_2, col_card_3 = st.columns(3)
with col_card_1:
    tahun_terakhir, total = healty_controller.total_for_last_year(df_combined, 'dokter')
    st.metric(f"Jumlah Dokter {tahun_terakhir}", f"{total}")

with col_card_2:
    tahun_terakhir, total = healty_controller.total_for_last_year(df_combined, 'perawat')
    st.metric(f"Jumlah Perawat {tahun_terakhir}", f"{total}")
with col_card_3:
    tahun_terakhir, total = healty_controller.total_for_last_year(df_combined, 'bidan')
    st.metric(f"Jumlah Bidan {tahun_terakhir}", f"{total}")

col_card_1, col_card_2, col_card_3 = st.columns(3)
with col_card_1:
    tahun_terakhir, total = healty_controller.total_for_last_year(df_combined, 'dokter_gigi')
    st.metric(f"Jumlah Dokter Gigi {tahun_terakhir}", f"{total}")

with col_card_2:
    tahun_terakhir, total = healty_controller.total_for_last_year(df_combined, 'farmasi')
    st.metric(f"Jumlah Tenaga Farmasi {tahun_terakhir}", f"{total}")
with col_card_3:
    tahun_terakhir, total = healty_controller.total_for_last_year(df_combined, 'tenaga_gizi')
    st.metric(f"Jumlah Tenaga Gizi {tahun_terakhir}", f"{total}")

col_card_1, col_card_2, col_card_3 = st.columns(3)
with col_card_1:
    tahun_terakhir, total = healty_controller.total_for_last_year(df_combined, 'tenaga_kesehatan_masyarakat')
    st.metric(f"Tenaga Kesehatan Masyarakat {tahun_terakhir}", f"{total}")

with col_card_2:
    tahun_terakhir, total = healty_controller.total_for_last_year(df_combined, 'tenaga_kesehatan_lingkungan')
    st.metric(f"Tenaga Kesehatan Lingkungan {tahun_terakhir}", f"{total}")
with col_card_3:
    tahun_terakhir, total = healty_controller.total_for_last_year(df_combined, 'ahli_teknologi_laboratorium_medik')
    st.metric(f"ATLM {tahun_terakhir}", f"{total}")
   
# Tampilkan tabel data yang sudah difilter
st.dataframe(filtered_data)
