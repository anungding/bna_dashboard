import streamlit as st
import altair as alt

# Mengambil data dari session_state
if "pendidikan_controller" in st.session_state:
    df_pendidikan = st.session_state["pendidikan_controller"].get_data()

    # Mengelompokkan berdasarkan kolom 'Kecamatan' dan menghitung jumlah murid per kecamatan
    jumlah_murid_per_kecamatan = df_pendidikan.groupby('kecamatan')['murid_negeri_swasta'].sum().reset_index()

    # Menampilkan hasil
    st.write(jumlah_murid_per_kecamatan)

    # Membuat bar chart dengan Altair
    chart = alt.Chart(jumlah_murid_per_kecamatan).mark_bar().encode(
        x=alt.X('kecamatan:N', title='Kecamatan'),
        y=alt.Y('murid_negeri_swasta:Q', title='Total Murid Negeri dan Swasta'),
        color='kecamatan:N'  # Warna berdasarkan kecamatan
    ).properties(
        title="Jumlah Murid Negeri Swasta per Kecamatan"
    )

    # Menampilkan chart di Streamlit
    st.altair_chart(chart, use_container_width=True)

    st.write(df_pendidikan)  # Menampilkan data pendidikan SMK
else:
    st.warning("Data pendidikan belum dimuat.")
