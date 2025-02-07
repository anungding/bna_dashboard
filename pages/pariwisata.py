import streamlit as st
import altair as alt
import pandas as pd
from controllers.pariwisata_controller import load_and_combine_data, get_filtered_data

# # Load data
df_combined, tahun_list, bulan_list, nama_wisata_list = load_and_combine_data()

# Tampilan Streamlit
st.title("DATA PARIWISATA BNA")

# Dropdown filter
col1, col2, col3 = st.columns(3)
with col1:
    tahun_option = st.selectbox("Pilih Tahun", tahun_list, index=0)
with col2:
    bulan_option = st.selectbox("Pilih Bulan", bulan_list, index=0)
with col3:
    nama_wisata_option = st.selectbox("Pilih Nama Wisata", nama_wisata_list, index=0)

# Filter data
filtered_data = get_filtered_data(df_combined, tahun_option, bulan_option, nama_wisata_option)
st.dataframe(filtered_data)

# Menampilkan Total Pengunjung dan Wisata
if not filtered_data.empty:
    total_pengunjung = filtered_data['kunjungan'].sum()
    total_wisata = len(filtered_data['nama'].unique())

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Total Keseluruhan Pengunjung", value=f"{int(total_pengunjung)}")
    with col2:
        st.metric(label="Total Wisata", value=f"{total_wisata}")

# Chart Total Pengunjung per Tahun
if not filtered_data.empty:
    st.subheader("Total Pengunjung per Tahun")
    grouped_by_tahun = filtered_data.groupby('tahun', as_index=False)['kunjungan'].sum()
    chart = alt.Chart(grouped_by_tahun).mark_bar().encode(
        x='tahun:N', y='kunjungan:Q', color='tahun:N', tooltip=['tahun', 'kunjungan']
    ).properties(title="Jumlah Kunjungan Wisata")
    st.altair_chart(chart, use_container_width=True)

# Chart Total Pengunjung per Bulan
if not filtered_data.empty:
    st.subheader("Total Pengunjung per Bulan")
    bulan_order = ["JANUARI", "PEBRUARI", "MARET", "APRIL", "MEI", "JUNI",
                   "JULI", "AGUSTUS", "SEPTEMBER", "OKTOBER", "NOPEMBER", "DESEMBER"]
    grouped_by_bulan = filtered_data.groupby('bulan', as_index=False)['kunjungan'].sum()
    grouped_by_bulan['bulan'] = pd.Categorical(grouped_by_bulan['bulan'], categories=bulan_order, ordered=True)
    grouped_by_bulan = grouped_by_bulan.sort_values('bulan')

    chart = alt.Chart(grouped_by_bulan).mark_bar().encode(
        x='bulan:N', y='kunjungan:Q', color='bulan:N', tooltip=['bulan', 'kunjungan']
    ).properties(title="Jumlah Kunjungan Wisata")
    st.altair_chart(chart, use_container_width=True)

# Chart Total Pengunjung per Tempat Wisata
if not filtered_data.empty:
    st.subheader("Total Pengunjung per Tempat Wisata")
    grouped_by_nama = filtered_data.groupby('nama', as_index=False)['kunjungan'].sum()
    chart = alt.Chart(grouped_by_nama).mark_bar().encode(
        x='nama:N', y='kunjungan:Q', color='nama', tooltip=['nama', 'kunjungan']
    ).properties(title="Jumlah Kunjungan Wisata")
    st.altair_chart(chart, use_container_width=True)
