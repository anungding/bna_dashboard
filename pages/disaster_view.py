import streamlit as st
import altair as alt
from streamlit_card import card
from controllers.disaster_controller import DisasterController
# from streamlit_elements import st_elements

st.title("DATA BENCANA BNA 🌋")
st.markdown("Silakan pilih filter yang sesuai untuk melihat data yang relevan dengan kebutuhan Anda.")

# Pastikan controller tersedia di session state
if "disaster_controller" not in st.session_state:
    st.session_state["disaster_controller"] = DisasterController()

disaster_controller = st.session_state["disaster_controller"]

# Ambil data yang sudah diproses
df_combined = disaster_controller.data

if df_combined.empty:
    st.error("Tidak ada data yang berhasil dimuat!")
else:
    # Pilihan filter
    tahun_options = ["Semua Tahun"] + list(df_combined['Tahun'].unique())
    kategori_options = ["Semua Kategori"] + list(df_combined['Kategori'].unique())
    kecamatan_options = ["Semua Kecamatan"] + list(df_combined['Kecamatan'].unique())

    col1, col2, col3 = st.columns(3)
    with col1:
        tahun_filter = st.selectbox("Pilih Tahun", tahun_options)
    with col2:
        kategori_filter = st.selectbox("Pilih Kategori", kategori_options)
    with col3:
        kecamatan_filter = st.selectbox("Pilih Kecamatan", kecamatan_options)

    # Filter data
    filtered_data = disaster_controller.filter_data(tahun_filter, kategori_filter, kecamatan_filter)

    st.markdown(
        f'Data yang difilter berdasarkan Tahun: <span style="color:red">{tahun_filter}</span>, '
        f'Kategori: <span style="color:red">{kategori_filter}</span>, '
        f'Kecamatan: <span style="color:red">{kecamatan_filter}</span>',
        unsafe_allow_html=True
    )


    # Perhitungan total
    if not filtered_data.empty:
        total_semua_tahun = filtered_data['Total'].sum()
        total_semua_kategori =  filtered_data['Kategori'].nunique()

        total_kategori_paling_banyak = filtered_data.groupby('Kategori')['Total'].sum()
        kategori_terbanyak = total_kategori_paling_banyak.idxmax()

        total_bulan_paling_banyak = disaster_controller.get_total_per_bulan(filtered_data)
        bulan_terbanyak = total_bulan_paling_banyak.loc[total_bulan_paling_banyak['Total'].idxmax()]
        bulan_terbanyak_nama = bulan_terbanyak['Bulan']

        total_tahun_paling_banyak = filtered_data.groupby('Tahun')['Total'].sum()
        tahun_terbanyak = total_tahun_paling_banyak.idxmax()  # Menyimpan tahun dengan bencana terbanyak
    
       
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(label="Total Banyak Bencana", value= f"{int(total_semua_tahun):,}")
        col2.metric(label="Bulan dengan Bencana Terbanyak", value=f"{bulan_terbanyak_nama}")
        col3.metric(label="Tahun dengan Bencana Terbanyak", value=f"{tahun_terbanyak}")
        col4.metric(label="Kategori dengan Bencana Terbanyak", value=f"{kategori_terbanyak}")

        col_chart_tahun, col_chart_bulan = st.columns(2)
        with col_chart_tahun:
            # **Chart Total Bencana per Tahun**
            grouped_by_tahun = disaster_controller.get_grouped_data(filtered_data, 'Tahun')
            st.subheader("Total Bencana per Tahun")
            st.markdown(
                f'Data yang difilter berdasarkan Tahun: <span style="color:red">{tahun_filter}</span>, '
                f'Kategori: <span style="color:red">{kategori_filter}</span>, '
                f'Kecamatan: <span style="color:red">{kecamatan_filter}</span>',
                unsafe_allow_html=True
            )
            chart_tahun = alt.Chart(grouped_by_tahun).mark_bar().encode(
                x='Tahun:N', y='Total:Q', color='Tahun:N', tooltip=['Tahun', 'Total']
            ).properties(width=600, height=400)
            st.altair_chart(chart_tahun, use_container_width=True)
        with col_chart_bulan:
            # **Chart Total Bencana per Bulan**
            total_per_bulan = disaster_controller.get_total_per_bulan(filtered_data)
            st.subheader("Total Bencana per Bulan")
            st.markdown(
                f'Data yang difilter berdasarkan Tahun: <span style="color:red">{tahun_filter}</span>, '
                f'Kategori: <span style="color:red">{kategori_filter}</span>, '
                f'Kecamatan: <span style="color:red">{kecamatan_filter}</span>',
                unsafe_allow_html=True
            )
            bulan_order = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Juni', 'Jul', 'Agt', 'Sept', 'Okt', 'Nop', 'Des']
            chart_bulan = alt.Chart(total_per_bulan).mark_bar().encode(
                x=alt.X('Bulan:N', sort=bulan_order),   # 'Bulan' sudah terurut dalam DataFrame
                y='Total:Q',
                color=alt.Color('Bulan:N', sort=bulan_order), 
                tooltip=['Bulan', 'Total']
            ).properties(width=600, height=400)

            st.altair_chart(chart_bulan, use_container_width=True)
    
        # **Chart Total Bencana per Kategori**
        grouped_by_tahun = disaster_controller.get_grouped_data(filtered_data, 'Kategori')
        st.subheader("Total Bencana per Kategori")
        st.markdown(
            f'Data yang difilter berdasarkan Tahun: <span style="color:red">{tahun_filter}</span>, '
            f'Kategori: <span style="color:red">{kategori_filter}</span>, '
            f'Kecamatan: <span style="color:red">{kecamatan_filter}</span>',
            unsafe_allow_html=True
        )
        chart_tahun = alt.Chart(grouped_by_tahun).mark_bar().encode(
            x='Kategori:N', y='Total:Q', color='Kategori:N', tooltip=['Kategori', 'Total']
        ).properties(width=600, height=400)
        st.altair_chart(chart_tahun, use_container_width=True)

        # **Chart Total Bencana per Kecamatan**
        grouped_by_tahun = disaster_controller.get_grouped_data(filtered_data, 'Kecamatan')
        st.subheader("Total Bencana per Kecamatan")
        st.markdown(
            f'Data yang difilter berdasarkan Tahun: <span style="color:red">{tahun_filter}</span>, '
            f'Kategori: <span style="color:red">{kategori_filter}</span>, '
            f'Kecamatan: <span style="color:red">{kecamatan_filter}</span>',
            unsafe_allow_html=True
        )
        chart_tahun = alt.Chart(grouped_by_tahun).mark_bar().encode(
            x='Kecamatan:N', y='Total:Q', color='Kecamatan:N', tooltip=['Kecamatan', 'Total']
        ).properties(width=600, height=400)
        st.altair_chart(chart_tahun, use_container_width=True)


        st.subheader("DATASET")
        st.markdown(
            f'Data yang difilter berdasarkan Tahun: <span style="color:red">{tahun_filter}</span>, '
            f'Kategori: <span style="color:red">{kategori_filter}</span>, '
            f'Kecamatan: <span style="color:red">{kecamatan_filter}</span>',
            unsafe_allow_html=True
        )
        st.dataframe(filtered_data, use_container_width=True)

        # Unduh data
        csv = disaster_controller.convert_df(filtered_data)
        st.download_button("Unduh Data yang Diperbarui", data=csv, file_name='data_filtered.csv', mime='text/csv')
        # Keterangan Sumber Data
        st.markdown(
            """
            ###### Sumber Dataset: BANJARNEGARA SATU DATA
            """
        )

