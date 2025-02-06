import streamlit as st

st.title("DASHBOARD BNA")

st.markdown(
"""
#### Selamat Datang,
Kami percaya bahwa data adalah kunci untuk pengambilan keputusan yang lebih baik. Oleh karena itu, kami menghadirkan BNA DASHBOARD, sebuah platform open-source yang menyediakan data, dashboard, dan visualisasi interaktif untuk mendukung transparansi, inovasi, dan kemajuan di BNA.
"""
)

# Membuat tiga kolom untuk card
col1, col2, col3 = st.columns(3)

with col1:
    with st.container():
        if st.button("DATA PENDUDUK 👯", use_container_width=True):
            st.switch_page("pages/penduduk.py")

with col2:
    with st.container():
        if st.button("DATA BENCANA 🌋", use_container_width=True):
            st.switch_page("pages/bencana.py")

with col3:
    with st.container():
        if st.button("DATA KESEHATAN 🧑‍⚕️", use_container_width=True):
            st.switch_page("pages/kesehatan.py")

# Membuat tiga kolom lagi untuk baris kedua
col4, col5, col6 = st.columns(3)

with col4:
    with st.container():
        if st.button("DATA PENDIDIKAN 🎓", use_container_width=True):
            st.switch_page("pages/pendidikan.py")

with col5:
    with st.container():
        if st.button("DATA PARIWISATA 🚠", use_container_width=True):
            st.switch_page("pages/pariwisata.py")

with col6:
    with st.container():
        if st.button("GIS 🗺️", use_container_width=True):
            st.switch_page("pages/gis.py")

st.markdown(
"""
#### Apa yang bisa anda akeses?
- Akses Data Terbuka. 
Menyediakan berbagai data resmi dan komunitas dalam satu tempat yang mudah diakses.
- Dashboard Interaktif.
Memvisualisasikan data dalam bentuk grafik dan laporan yang mudah dipahami.
- Kolaborasi dan Keterbukaan.
Mengusung prinsip open-source, sehingga siapa pun dapat berkontribusi dan mengembangkan fitur lebih lanjut.

#### Untuk Siapa Aplikasi Ini?
- Pemerintah Daerah.
Mendukung pengambilan kebijakan berbasis data.
- Peneliti & Akademisi.
Menyediakan data yang dapat digunakan untuk analisis dan penelitian.
Masyarakat Umum.
Meningkatkan transparansi dan partisipasi warga dalam memahami perkembangan daerah mereka.

Bersama, mari wujudkan ekosistem data terbuka untuk membangun daerah yang lebih cerdas dan berkelanjutan!
"""
)