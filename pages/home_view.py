import streamlit as st

# Judul utama dari dashboard
st.title("DASHBOARD BNA ⏹️")

st.markdown('<span style="color:red">Gunakan perangkat dengan layar besar dan resolusi lebih tinggi dari 720p untuk tampilan yang lebih baik.</span>', unsafe_allow_html=True)

# Penjelasan singkat tentang dashboard BNA
st.markdown(
"""
Kami percaya bahwa data adalah kunci untuk pengambilan keputusan yang lebih baik. Oleh karena itu, kami menghadirkan BNA DASHBOARD, sebuah platform open-source yang menyediakan data, dashboard, dan visualisasi interaktif untuk mendukung transparansi, inovasi, dan kemajuan di BNA.
"""
)

# Membuat tiga kolom untuk card pertama
col1, col2, col3 = st.columns(3)

with col1:
    with st.container():
        # Tombol untuk mengakses data penduduk
        if st.button("DATA PENDUDUK 👯", use_container_width=True):
            st.switch_page("pages/penduduk.py")

with col2:
    with st.container():
        # Tombol untuk mengakses data bencana
        if st.button("DATA BENCANA 🌋", use_container_width=True):
            st.switch_page("pages/bencana.py")

with col3:
    with st.container():
        # Tombol untuk mengakses data kesehatan
        if st.button("DATA KESEHATAN 🧑‍⚕️", use_container_width=True):
            st.switch_page("pages/kesehatan.py")

# Membuat tiga kolom lagi untuk baris kedua
col4, col5, col6 = st.columns(3)

with col4:
    with st.container():
        # Tombol untuk mengakses data pendidikan
        if st.button("DATA PENDIDIKAN 🎓", use_container_width=True):
            st.switch_page("pages/pendidikan.py")

with col5:
    with st.container():
        # Tombol untuk mengakses data pariwisata
        if st.button("DATA PARIWISATA 🚠", use_container_width=True):
            st.switch_page("pages/pariwisata.py")

with col6:
    with st.container():
        # Tombol untuk mengakses data GIS
        if st.button("GIS 🗺️", use_container_width=True):
            st.switch_page("pages/gis.py")

# Membuat dua kolom untuk informasi tambahan
col7, col8 = st.columns(2)

with col7:
    # Penjelasan tentang fitur-fitur yang dapat diakses di aplikasi
    st.markdown(
    """
    #### Apa yang bisa anda akeses?
    - **Akses Data Terbuka.** 
    Menyediakan berbagai data resmi dan komunitas dalam satu tempat yang mudah diakses.
    - **Dashboard Interaktif.**
    Memvisualisasikan data dalam bentuk grafik dan laporan yang mudah dipahami.
    - **Kolaborasi dan Keterbukaan.**
    Mengusung prinsip open-source, sehingga siapa pun dapat berkontribusi dan mengembangkan fitur lebih lanjut.
    """
    )

with col8:
    # Penjelasan tentang siapa saja yang bisa menggunakan aplikasi
    st.markdown("""
    #### Untuk Siapa Aplikasi Ini?
    - **Pemerintah Daerah.**
    Mendukung pengambilan kebijakan berbasis data.
    - **Peneliti & Akademisi.**
    Menyediakan data yang dapat digunakan untuk analisis dan penelitian.
    - **Masyarakat Umum.**
    Meningkatkan transparansi dan partisipasi warga dalam memahami perkembangan daerah mereka.
    """)
    
# Informasi tentang kontribusi pada proyek
st.markdown("""
#### Mau berkontribusi?
- Project 🚀[Github][https://github.com/anungding/bna_data](https://github.com/anungding/bna_data)
#### Bersama, mari wujudkan ekosistem data terbuka untuk membangun daerah yang lebih cerdas, maju, dan berkelanjutan!
""")
