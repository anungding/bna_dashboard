import streamlit as st
import altair as alt
from controllers.pariwisata_controller import PariwisataController

st.title("DATA PARIWISATA BNA")
st.markdown("Silakan pilih filter yang sesuai untuk melihat data yang relevan.")

# Inisialisasi controller
if "pariwisata_controller" not in st.session_state:
    st.session_state["pariwisata_controller"] = PariwisataController()
controller = st.session_state["pariwisata_controller"]

# Ambil data
if controller.data is None or controller.data.empty:
    st.error("Tidak ada data yang berhasil dimuat!")
else:
    # Pilihan filter
    tahun_options = ["All"] + sorted(controller.data['tahun'].unique())
    bulan_options = ["All"] + sorted(controller.data['bulan'].unique())
    nama_wisata_options = ["All"] + sorted(controller.data['nama'].unique())

    col1, col2, col3 = st.columns(3)
    with col1:
        tahun_filter = st.selectbox("Pilih Tahun", tahun_options)
    with col2:
        bulan_filter = st.selectbox("Pilih Bulan", bulan_options)
    with col3:
        nama_wisata_filter = st.selectbox("Pilih Nama Wisata", nama_wisata_options)

    # Filter data
    filtered_data = controller.get_filtered_data(tahun_filter, bulan_filter, nama_wisata_filter)

    st.write(f"Data yang difilter berdasarkan Tahun: {tahun_filter}, Bulan: {bulan_filter}, Nama Wisata: {nama_wisata_filter}")


    if not filtered_data.empty:
        col_chart_tahun, col_chart_bulan = st.columns(2)

        with col_chart_tahun:
            # **Chart Total Kunjungan per Tahun**
            st.subheader("Total Kunjungan per Tahun")
            st.write(f"Data yang difilter berdasarkan Tahun: {tahun_filter}, Bulan: {bulan_filter}, Nama Wisata: {nama_wisata_filter}")
            grouped_by_tahun = controller.get_grouped_data(filtered_data, 'tahun')
            chart_tahun = alt.Chart(grouped_by_tahun).mark_bar().encode(
                x='tahun:N', y='kunjungan:Q', color='tahun:N', tooltip=['tahun', 'kunjungan']
            ).properties(width=600, height=400)
            st.altair_chart(chart_tahun, use_container_width=True)

        with col_chart_bulan:
            # **Chart Total Kunjungan per Bulan**
            st.subheader("Total Kunjungan per Bulan")
            st.write(f"Data yang difilter berdasarkan Tahun: {tahun_filter}, Bulan: {bulan_filter}, Nama Wisata: {nama_wisata_filter}")
            total_per_bulan = controller.get_total_per_bulan(filtered_data)
            chart_bulan = alt.Chart(total_per_bulan).mark_bar().encode(
                x='Bulan:N', y='Total:Q', color='Bulan:N', tooltip=['Bulan', 'Total']
            ).properties(width=600, height=400)
            st.altair_chart(chart_bulan, use_container_width=True)

        # **Chart Total Kunjungan per Wisata**
        st.subheader("Total Kunjungan per Tempat Wisata")
        st.write(f"Data yang difilter berdasarkan Tahun: {tahun_filter}, Bulan: {bulan_filter}, Nama Wisata: {nama_wisata_filter}")
        grouped_by_nama = controller.get_grouped_data(filtered_data, 'nama')
        chart_nama = alt.Chart(grouped_by_nama).mark_bar().encode(
            x='nama:N', y='kunjungan:Q', color='nama:N', tooltip=['nama', 'kunjungan']
        ).properties(width=600, height=400)
        st.altair_chart(chart_nama, use_container_width=True)


        st.subheader("DATASET")
        # **Keterangan Filter Data
        st.write(f"Data yang difilter berdasarkan Tahun: {tahun_filter}, Bulan: {bulan_filter}, Nama Wisata: {nama_wisata_filter}")
        st.dataframe(filtered_data, use_container_width=True)

        # Unduh data
        csv = controller.convert_df(filtered_data)
        st.download_button("Unduh Data yang Diperbarui", data=csv, file_name='data_pariwisata_filtered.csv', mime='text/csv')

        # Keterangan Sumber Data
        st.markdown(
            """
            ###### Sumber Dataset: BANJARNEGARA SATU DATA
            """
        )