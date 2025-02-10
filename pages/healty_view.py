import streamlit as st
import altair as alt
from controllers.healty_controller import HealtyController

# Inisialisasi controller
healty_controller = HealtyController()

st.title("DATA KESEHATAN BNA 🚑🧑‍⚕️🦠")
st.markdown("""---""")
st.subheader("DATA TENAGA KESEHATAN BNA 🧑‍⚕️")

# **Cek dan Simpan Data di Session State**
if 'df_combined' not in st.session_state:
    st.session_state['df_combined'] = healty_controller.get_combined_data()

df_combined = st.session_state['df_combined']

# **Pengecekan Jika Data Kosong**
if df_combined.empty:
    st.warning("Data tidak tersedia. Silakan periksa kembali sumber data.")
    st.stop()  # Hentikan eksekusi kode di bawah jika data kosong

# **Filter Tahun & Kecamatan**
years = df_combined['tahun'].unique()
kecamatans = df_combined['kecamatan'].unique()

col_sel_fil_1, col_sel_fil_2 = st.columns(2)
with col_sel_fil_1:
    selected_year = st.selectbox("Pilih Tahun", options=['Semua Tahun'] + list(years), index=0)
with col_sel_fil_2:
    selected_kecamatan = st.selectbox("Pilih Kecamatan", options=['Semua Kecamatan'] + list(kecamatans), index=0)

# **Cek dan Simpan Filtered Data di Session State**
if 'filtered_data' not in st.session_state or st.session_state['selected_year'] != selected_year or st.session_state['selected_kecamatan'] != selected_kecamatan:
    st.session_state['filtered_data'] = healty_controller.filter_data(df_combined, selected_year, selected_kecamatan)
    st.session_state['selected_year'] = selected_year
    st.session_state['selected_kecamatan'] = selected_kecamatan

filtered_data = st.session_state['filtered_data']

# **Pengecekan Jika Data Hasil Filter Kosong**
if filtered_data.empty:
    st.warning("Tidak ada data untuk filter yang dipilih.")
    st.stop()  # Hentikan eksekusi jika data hasil filter kosong

# **Metric Cards**
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

# **Sebaran Tenaga Kesehatan per Kecamatan**
columns_kesehatan = ['dokter', 'perawat', 'bidan', 'dokter_gigi', 'farmasi', 'tenaga_gizi', 
                     'tenaga_kesehatan_masyarakat', 'tenaga_kesehatan_lingkungan', 'ahli_teknologi_laboratorium_medik']

sebaran_tenaga_kesehatan = filtered_data.groupby('kecamatan')[columns_kesehatan].sum().reset_index()
sebaran_tenaga_kesehatan = sebaran_tenaga_kesehatan.melt(id_vars=['kecamatan'], value_vars=columns_kesehatan, 
                                                         var_name='Jenis Tenaga Kesehatan', value_name='Jumlah')

st.subheader("Total Tenaga Kesehatan per Kecamatan")
st.markdown(
    f'Data yang difilter berdasarkan Tahun: <span style="color:red">{selected_year} </span>, '
    f'Kecamatan: <span style="color:red">{selected_year}</span>',              
    unsafe_allow_html=True
)
chart = alt.Chart(sebaran_tenaga_kesehatan).mark_bar().encode(
    y=alt.Y('kecamatan:N', title='Kecamatan', sort='-x'),
    x=alt.X('Jumlah:Q', title='Jumlah Tenaga Kesehatan'),
    color='Jenis Tenaga Kesehatan:N',
    tooltip=['kecamatan', 'Jenis Tenaga Kesehatan', 'Jumlah']
).properties(
    width=700,
    height=600
)

st.altair_chart(chart, use_container_width=True)

# **Terapkan Filter Kecamatan ke Data**
if selected_kecamatan != 'Semua Kecamatan':
    df_filtered_kesehatan = df_combined[df_combined['kecamatan'] == selected_kecamatan]
else:
    df_filtered_kesehatan = df_combined

# **Sebaran Tenaga Kesehatan per Tahun (dengan filter Kecamatan)**
columns_kesehatan = ['dokter', 'perawat', 'bidan', 'dokter_gigi', 'farmasi', 'tenaga_gizi', 
                     'tenaga_kesehatan_masyarakat', 'tenaga_kesehatan_lingkungan', 'ahli_teknologi_laboratorium_medik']

kesehatan_per_tahun = df_filtered_kesehatan.groupby(['tahun'])[columns_kesehatan].sum().reset_index()
kesehatan_per_tahun = kesehatan_per_tahun.melt(id_vars=['tahun'], var_name='Jenis Tenaga Kesehatan', value_name='Jumlah')

st.subheader(f"Total Tenaga Kesehatan dari Tahun ke Tahun ({selected_kecamatan})")
st.markdown(
    f'Data yang difilter berdasarkan Tahun: <span style="color:red">{selected_year} </span>, '
    f'Kecamatan: <span style="color:red">{selected_year}</span>',              
    unsafe_allow_html=True
)
chart_tahunan = alt.Chart(kesehatan_per_tahun).mark_line(point=True).encode(
    x=alt.X('tahun:O', title='Tahun'),
    y=alt.Y('Jumlah:Q', title='Jumlah Tenaga Kesehatan'),
    color='Jenis Tenaga Kesehatan:N',
    tooltip=['tahun', 'Jenis Tenaga Kesehatan', 'Jumlah']
).properties(
    width=700,
    height=500
)

st.altair_chart(chart_tahunan, use_container_width=True)


# **Dataset Table**
st.subheader("DATASET")
st.markdown(
    f'Data yang difilter berdasarkan Tahun: <span style="color:red">{selected_year} </span>, '
    f'Kecamatan: <span style="color:red">{selected_year}</span>',            
    unsafe_allow_html=True
)
st.dataframe(filtered_data)

csv = healty_controller.convert_df(filtered_data)
st.download_button("Unduh Data yang Diperbarui", data=csv, file_name='healty_filtered.csv', mime='text/csv')

# **Sumber Data**
st.markdown("###### Sumber Dataset: BANJARNEGARA SATU DATA")
