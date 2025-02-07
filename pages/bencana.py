import streamlit as st
import altair as alt
from controllers.bencana_controller import BencanaController

st.title("DATA BENCANA BNA")
st.markdown("Silakan pilih filter yang sesuai untuk melihat data yang relevan dengan kebutuhan Anda.")

# Pastikan controller tersedia di session state
if "bencana_controller" not in st.session_state:
    st.session_state["bencana_controller"] = BencanaController()

bencana_controller = st.session_state["bencana_controller"]

# Ambil data yang sudah diproses
df_combined = bencana_controller.data

if df_combined.empty:
    st.error("Tidak ada data yang berhasil dimuat!")
else:
    # Pilihan filter
    tahun_options = ["All"] + list(df_combined['Tahun'].unique())
    kategori_options = ["All"] + list(df_combined['Kategori'].unique())
    kecamatan_options = ["All"] + list(df_combined['Kecamatan'].unique())

    col1, col2, col3 = st.columns(3)
    with col1:
        tahun_filter = st.selectbox("Pilih Tahun", tahun_options)
    with col2:
        kategori_filter = st.selectbox("Pilih Kategori", kategori_options)
    with col3:
        kecamatan_filter = st.selectbox("Pilih Kecamatan", kecamatan_options)

    # Filter data
    filtered_data = bencana_controller.filter_data(tahun_filter, kategori_filter, kecamatan_filter)

    st.write(f"Data yang difilter berdasarkan Tahun: {tahun_filter}, Kategori: {kategori_filter}, Kecamatan: {kecamatan_filter}")
    st.dataframe(filtered_data, use_container_width=True)

    # Unduh data
    csv = bencana_controller.convert_df(filtered_data)
    st.download_button("Unduh Data yang Diperbarui", data=csv, file_name='data_filtered.csv', mime='text/csv')

    # Perhitungan total
    if not filtered_data.empty:
        total_semua_tahun = filtered_data['Total'].sum()
        st.metric("Total Keseluruhan Bencana", f"{total_semua_tahun}")

        # **Chart Total Bencana per Tahun**
        grouped_by_tahun = bencana_controller.get_grouped_data(filtered_data, 'Tahun')
        st.subheader("Total Bencana per Tahun")
        chart_tahun = alt.Chart(grouped_by_tahun).mark_bar().encode(
            x='Tahun:N', y='Total:Q', color='Tahun:N', tooltip=['Tahun', 'Total']
        ).properties(width=600, height=400)
        st.altair_chart(chart_tahun, use_container_width=True)

        # **Chart Total Bencana per Bulan**
        total_per_bulan = bencana_controller.get_total_per_bulan(filtered_data)
        st.subheader("Total Bencana per Bulan")
        chart_bulan = alt.Chart(total_per_bulan).mark_bar().encode(
            x='Bulan:N', y='Total:Q', color='Bulan:N', tooltip=['Bulan', 'Total']
        ).properties(width=600, height=400)
        st.altair_chart(chart_bulan, use_container_width=True)

        # **Chart Total Bencana per Kategori**
        grouped_by_tahun = bencana_controller.get_grouped_data(filtered_data, 'Kategori')
        st.subheader("Total Bencana per Kategori")
        chart_tahun = alt.Chart(grouped_by_tahun).mark_bar().encode(
            x='Kategori:N', y='Total:Q', color='Kategori:N', tooltip=['Kategori', 'Total']
        ).properties(width=600, height=400)
        st.altair_chart(chart_tahun, use_container_width=True)

        # **Chart Total Bencana per Kecamatan**
        grouped_by_tahun = bencana_controller.get_grouped_data(filtered_data, 'Kecamatan')
        st.subheader("Total Bencana per Kecamatan")
        chart_tahun = alt.Chart(grouped_by_tahun).mark_bar().encode(
            x='Kecamatan:N', y='Total:Q', color='Kecamatan:N', tooltip=['Kecamatan', 'Total']
        ).properties(width=600, height=400)
        st.altair_chart(chart_tahun, use_container_width=True)
