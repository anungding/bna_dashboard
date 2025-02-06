import os
import pandas as pd
import altair as alt
import streamlit as st

# Judul aplikasi di Streamlit
st.title("DATA PARIWISATA BNA")

# Folder tempat menyimpan file CSV
dataset_folder = 'dataset/pariwisata/'

#-------------GLOBAL VARIABEL-----------------


bulan_order = ["JANUARI", "PEBRUARI", "MARET", "APRIL", "MEI", "JUNI", 
               "JULI", "AGUSTUS", "SEPTEMBER", "OKTOBER", "NOPEMBER", "DESEMBER"]

filtered_data = pd.DataFrame()

# Fungsi untuk memuat file CSV secara otomatis dari folder
def load_data_from_folder(folder):
    data_files = {}

    for file_name in os.listdir(folder):
        if file_name.endswith('.csv'):
            parts = file_name[:-4].split('_')

            if len(parts) < 2:
                continue  
            
            if parts[-1].isdigit():
                tahun = parts[-1]
                nama = "_".join(parts[:-1])  
            else:
                continue  

            if nama not in data_files:
                data_files[nama] = []
            
            file_path = os.path.join(folder, file_name)
            data_files[nama].append((file_path, int(tahun)))

    return data_files

# Memuat data dari folder dataset
data_files = load_data_from_folder(dataset_folder)

try:
    data_frames = []
    tahun_list = set()
    bulan_list = set()
    nama_wisata_list = set()

    for nama, files in data_files.items():
        for file_path, tahun in files:
            try:
                df = pd.read_csv(file_path, sep=',')
               
                df.replace("-", 0, inplace=True)
                df.replace(r"^\s*-+\s*$", "0", regex=True, inplace=True)

                df.columns = df.columns.str.strip().str.lower()

                df['bulan'] = df['bulan'].str.strip()
                df['bulan'] = df['bulan'].replace("JAN", "JANUARI")
                df['bulan'] = df['bulan'].replace("MAR", "MARET")
                df['bulan'] = df['bulan'].replace("APR", "APRIL")
                df['bulan'] = df['bulan'].replace("AGS", "AGUSTUS")
                df['bulan'] = df['bulan'].replace("JUL", "JULI")
                df['bulan'] = df['bulan'].replace("JUN", "JUNI")
                df['bulan'] = df['bulan'].replace("SEP", "SEPTEMBER")
                df['bulan'] = df['bulan'].replace("OKT", "OKTOBER")
                df['bulan'] = df['bulan'].replace("FEB", "PEBRUARI")
                df['bulan'] = df['bulan'].replace("NOP", "NOPEMBER")
                df['bulan'] = df['bulan'].replace("DES", "DESEMBER")

                # Normalisasi nama kolom 'pengunjung' menjadi 'kunjungan'
                df = df.rename(columns={'pengunjung': 'kunjungan'})

                # Jika ada kedua kolom, jumlahkan dan hapus duplikat
                if 'kunjungan' in df.columns and 'pengunjung' in df.columns:
                    df['kunjungan'] = df[['kunjungan', 'pengunjung']].sum(axis=1)
                    df.drop(columns=['pengunjung'], inplace=True)
                
            
                # Hapus baris jika kolom 'bulan' bernilai None atau NaN
                if 'bulan' in df.columns:
                    df = df.dropna(subset=['bulan'])

                # Format angka di kolom 'kunjungan' dengan menghapus koma
                if 'kunjungan' in df.columns:
                    df['kunjungan'] = df['kunjungan'].astype(str).str.replace(',', '').astype(float)

                # Ganti NaN di 'kunjungan' dengan 0
                if 'kunjungan' in df.columns:
                    df['kunjungan'] = df['kunjungan'].fillna(0)   

                df['tahun'] = str(tahun)
                df['nama'] = nama

                col_order = ['nama', 'tahun', 'bulan'] + [col for col in df.columns if col not in ['nama', 'tahun', 'bulan']]
                df = df[[col for col in col_order if col in df.columns]]  

                data_frames.append(df)

                # Mengumpulkan tahun, bulan, dan nama wisata unik
                tahun_list.add(tahun)
                bulan_list.update(df['bulan'].unique())
                nama_wisata_list.add(nama)

            except FileNotFoundError:
                st.warning(f"File tidak ditemukan: {file_path}")
            except Exception as e:
                st.warning(f"Kesalahan saat membaca file {file_path}: {e}")

    if data_frames:
        df_combined = pd.concat(data_frames, ignore_index=True)

        # Menambahkan "All" ke dalam pilihan filter
        tahun_list = ["All"] + sorted(tahun_list)
        bulan_list = ["All"] + sorted(bulan_list)
        nama_wisata_list = ["All"] + sorted(nama_wisata_list)

        # Membuat kolom filter secara horizontal
        col1, col2, col3 = st.columns(3)

        with col1:
            # Filter berdasarkan tahun
            tahun_option = st.selectbox("Pilih Tahun", tahun_list, index=0)

        with col2:
            # Filter berdasarkan bulan
            bulan_option = st.selectbox("Pilih Bulan", bulan_list, index=0)

        with col3:
            # Filter berdasarkan nama wisata
            nama_wisata_option = st.selectbox("Pilih Nama Wisata", nama_wisata_list, index=0)

        # Menampilkan informasi filter yang dipilih
        st.write(f"Data yang difilter berdasarkan Tahun: {tahun_option}, Bulan: {bulan_option}, Nama Wisata: {nama_wisata_option}")

        
        # Memfilter data berdasarkan pilihan
        filtered_data = df_combined  # Menyimpan data yang sudah difilter di variabel global

        if tahun_option != "All":
            filtered_data = filtered_data[filtered_data['tahun'] == str(tahun_option)]
        if bulan_option != "All":
            filtered_data = filtered_data[filtered_data['bulan'] == bulan_option]
        if nama_wisata_option != "All":
            filtered_data = filtered_data[filtered_data['nama'] == nama_wisata_option]

        # Menampilkan dataframe yang sudah difilter
        st.dataframe(filtered_data)  

        @st.cache_data
        def convert_df(df):
            return df.to_csv(index=False).encode('utf-8')

        csv = convert_df(filtered_data)

        st.download_button(
            label="Unduh Data yang Diperbarui",
            data=csv,
            file_name='data_filtered.csv',
            mime='text/csv',
        )
except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")


#---------------------CARD--------------------------------
# MENAMPILKAN CARD TOTAL PENGUNJUNG DAN TOTAL WISATA YANG TERDAFTAR
if not filtered_data.empty:
    total_pengunjung = filtered_data['kunjungan'].sum()
    total_wisata = len( filtered_data['nama'].unique())

    # Menampilkan tiga metric (card)
    col1, col2 = st.columns(2)

    with col1:
        st.metric(label="Total Keselurahan Pengunjung", value=f"{int(total_pengunjung)}")

    with col2:
        st.metric(label="Total Wisata", value=f"{total_wisata}")


#-------------------BAR CHART----------------------------------
# Perhitungan Total Kunjungan/Pengunjung per Tahun
if not filtered_data.empty:
  
    grouped_by_tahun = filtered_data.groupby('tahun', as_index=False)['kunjungan'].sum()

    # Menampilkan chart Total Bencana per Tahun
    st.title("Total Pengunjung per Tahun")
    
    # Menampilkan informasi filter yang dipilih
    st.write(f"Data yang difilter berdasarkan Tahun: {tahun_option}, Bulan: {bulan_option}, Nama Wisata: {nama_wisata_option}")

    df = pd.DataFrame(grouped_by_tahun)

    # Membuat Bar Chart dengan Altair
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('tahun:N', title='Tahun'),
        y=alt.Y('kunjungan:Q', title='Total Kunjungan'),
        color='tahun:N', 
        tooltip=['tahun', 'kunjungan']
    ).properties(
        title='Jumlah Kunjungan Wisata'
    )

    # Menampilkan chart di Streamlit
    st.altair_chart(chart, use_container_width=True)

#-----------------------------------------------------
# Perhitungan Total Kunjungan/Pengunjung per Bulan
if not filtered_data.empty:

    grouped_by_bulan = filtered_data.groupby('bulan', as_index=False)['kunjungan'].sum()

    # Konversi 'bulan' ke tipe kategori dengan urutan yang benar
    grouped_by_bulan['bulan'] = pd.Categorical(grouped_by_bulan['bulan'], categories=bulan_order, ordered=True)

    # Urutkan DataFrame berdasarkan urutan bulan
    grouped_by_bulan = grouped_by_bulan.sort_values('bulan')

    # Menampilkan chart Total Bencana per Bulan
    st.title("Total Pengunjung per Bulan")
    
    # Menampilkan informasi filter yang dipilih
    st.write(f"Data yang difilter berdasarkan Tahun: {tahun_option}, Bulan: {bulan_option}, Nama Wisata: {nama_wisata_option}")

    df = pd.DataFrame(grouped_by_bulan)

     # Membuat Bar Chart dengan Altair
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('bulan:N',  sort=bulan_order, title='Bulan'),
        y=alt.Y('kunjungan:Q', title='Total Kunjungan'),  
        color='bulan:N', 
        tooltip=['bulan', 'kunjungan']
    ).properties(
        title='Jumlah Kunjungan Wisata'
    )


    # Menampilkan chart di Streamlit
    st.altair_chart(chart, use_container_width=True)

#-----------------------------------------------------
# Perhitungan Total Kunjungan/Pengunjung per Bulan
if not filtered_data.empty:

    grouped_by_nama = filtered_data.groupby('nama', as_index=False)['kunjungan'].sum()

    # Menampilkan chart Total Bencana per Bulan
    st.title("Total Pengunjung per Tempat Wisata")
    
    # Menampilkan informasi filter yang dipilih
    st.write(f"Data yang difilter berdasarkan Tahun: {tahun_option}, Bulan: {bulan_option}, Nama Wisata: {nama_wisata_option}")

    df = pd.DataFrame(grouped_by_nama)

    # Membuat Bar Chart
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('nama:N',  sort=bulan_order, title='Tempat Wisata'),
        y=alt.Y('kunjungan:Q', title='Total Kunjungan'),  
        color='nama', 
        tooltip=['nama', 'kunjungan']
    ).properties(
        title='Jumlah Kunjungan Wisata'
    )

    # Menampilkan chart
    st.altair_chart(chart, use_container_width=True)

