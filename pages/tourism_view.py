import streamlit as st
import altair as alt
from controllers.tourism_controller import TourismController

st.title("DATA PARIWISATA BNA 🚠")
st.markdown("Silakan pilih filter yang sesuai untuk melihat data yang relevan.")

# Inisialisasi controller
if "tourism_controller" not in st.session_state:
    st.session_state["tourism_controller"] = TourismController()
controller = st.session_state["tourism_controller"]

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

    st.markdown(
        f'Data yang difilter berdasarkan Tahun: <span style="color:red">{tahun_filter}</span>, '
        f'Bulan: <span style="color:red">{bulan_filter}</span>, '
        f'Tempat Wisata: <span style="color:red">{nama_wisata_filter}</span>',
        unsafe_allow_html=True
    )


   

    if not filtered_data.empty:

        total_semua_tahun = filtered_data['kunjungan'].sum()
 
        total_bulan_paling_banyak = filtered_data.groupby('bulan')['kunjungan'].sum()
        bulan_terbanyak_nama = total_bulan_paling_banyak.idxmax()


        total_nama_paling_banyak = filtered_data.groupby('nama')['kunjungan'].sum()
        nama_terbanyak = total_nama_paling_banyak.idxmax()


        total_tahun_paling_banyak = filtered_data.groupby('tahun')['kunjungan'].sum()
        tahun_terbanyak = total_tahun_paling_banyak.idxmax()  # Menyimpan tahun dengan bencana terbanyak
        
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(label="Total Banyak Wisatawan", value= f"{int(total_semua_tahun):,}")
        col2.metric(label="Bulan dengan Wisatawan Terbanyak", value=f"{bulan_terbanyak_nama}")
        col3.metric(label="Tahun dengan Wisatawan Terbanyak", value=f"{tahun_terbanyak}")
        col4.metric(label="Wisata dengan Wisatawan Terbanyak", value=f"{nama_terbanyak}")

        col_chart_tahun, col_chart_bulan = st.columns(2)

        with col_chart_tahun:
            # **Chart Total Kunjungan per Tahun**
            st.subheader("Total Kunjungan per Tahun")
            st.markdown(
                f'Data yang difilter berdasarkan Tahun: <span style="color:red">{tahun_filter}</span>, '
                f'Bulan: <span style="color:red">{bulan_filter}</span>, '
                f'Tempat Wisata: <span style="color:red">{nama_wisata_filter}</span>',
                unsafe_allow_html=True
            )
            grouped_by_tahun = controller.get_grouped_data(filtered_data, 'tahun')
            chart_tahun = alt.Chart(grouped_by_tahun).mark_bar().encode(
                x='tahun:N', y='kunjungan:Q', color='tahun:N', tooltip=['tahun', 'kunjungan']
            ).properties(width=600, height=400)
            st.altair_chart(chart_tahun, use_container_width=True)

        with col_chart_bulan:
            # **Chart Total Kunjungan per Bulan**
            st.subheader("Total Kunjungan per Bulan")
            st.markdown(
                f'Data yang difilter berdasarkan Tahun: <span style="color:red">{tahun_filter}</span>, '
                f'Bulan: <span style="color:red">{bulan_filter}</span>, '
                f'Tempat Wisata: <span style="color:red">{nama_wisata_filter}</span>',
                unsafe_allow_html=True
            )
            bulan_order = ["JANUARI", "PEBRUARI", "MARET", "APRIL", "MEI", "JUNI", 
                      "JULI", "AGUSTUS", "SEPTEMBER", "OKTOBER", "NOPEMBER", "DESEMBER"]
            total_per_bulan = controller.get_total_per_bulan(filtered_data)
            chart_bulan = alt.Chart(total_per_bulan).mark_bar().encode(
                y='Total:Q', x=alt.X('Bulan:N', sort=bulan_order), tooltip=['Bulan', 'Total'],
                color=alt.Color('Bulan:N', sort=bulan_order),
            ).properties(width=600, height=400)
            st.altair_chart(chart_bulan, use_container_width=True)

        # **Chart Total Kunjungan per Wisata**
        st.subheader("Total Kunjungan per Tempat Wisata")
        st.markdown(
            f'Data yang difilter berdasarkan Tahun: <span style="color:red">{tahun_filter}</span>, '
            f'Bulan: <span style="color:red">{bulan_filter}</span>, '
            f'Tempat Wisata: <span style="color:red">{nama_wisata_filter}</span>',
            unsafe_allow_html=True
        )
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