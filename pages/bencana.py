import streamlit as st
import pandas as pd
import os
import altair as alt

st.title("DATA BENCANA BNA")

# Kata pengantar
st.markdown("""
Silakan pilih filter yang sesuai untuk melihat data yang relevan dengan kebutuhan Anda.
""")

# Folder tempat menyimpan file CSV
dataset_folder = 'dataset/bencana/'

# Fungsi untuk memuat file CSV secara otomatis dari folder
def load_data_from_folder(folder):
    data_files = {}
    for file_name in os.listdir(folder):
        if file_name.endswith('.csv'):
            parts = file_name.split('_')
            if len(parts) == 2:
                kategori = parts[0]
                tahun = parts[1].replace('.csv', '')
            elif len(parts) == 3:
                kategori = parts[0] + "_" + parts[1]
                tahun = parts[2].replace('.csv', '')
            else:
                continue

            if kategori not in data_files:
                data_files[kategori] = []
            file_path = os.path.join(folder, file_name)
            data_files[kategori].append((file_path, int(tahun)))

    return data_files

# Load data secara otomatis dari folder
data_files = load_data_from_folder(dataset_folder)

# Deklarasikan filtered_data sebagai global sebelum digunakan
filtered_data = pd.DataFrame()

try:
    data_frames = []

    for kategori, files in data_files.items():
        for file_path, tahun in files:
            try:
                df = pd.read_csv(file_path, sep=';')
                df.columns = df.columns.str.strip()
                df.replace("-", 0, inplace=True)
                df['Tahun'] = str(tahun)
                df['Kategori'] = kategori

                col_order = ['Kecamatan', 'Kategori', 'Tahun'] + [col for col in df.columns if col not in ['Kecamatan', 'Kategori', 'Tahun']]
                df = df[col_order]

                for col in df.columns:
                    if col not in ['Kecamatan', 'Kategori', 'Tahun']:
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

                data_frames.append(df)

            except FileNotFoundError:
                st.warning(f"File tidak ditemukan: {file_path}")

    if data_frames:
        df_combined = pd.concat(data_frames, ignore_index=True)

        # Filter berdasarkan Tahun, Kecamatan, dan Kategori
        tahun_options = df_combined['Tahun'].unique()
        kategori_options = df_combined['Kategori'].unique()
        kecamatan_options = df_combined['Kecamatan'].unique()

        col1, col2, col3 = st.columns(3)

        with col1:
            tahun_filter = st.selectbox("Pilih Tahun", ["All"] + list(tahun_options))

        with col2:
            kategori_filter = st.selectbox("Pilih Kategori", ["All"] + list(kategori_options))

        with col3:
            kecamatan_filter = st.selectbox("Pilih Kecamatan", ["All"] + list(kecamatan_options))

        filtered_data = df_combined

        if tahun_filter != "All":
            filtered_data = filtered_data[filtered_data['Tahun'] == tahun_filter]

        if kategori_filter != "All":
            filtered_data = filtered_data[filtered_data['Kategori'] == kategori_filter]

        if kecamatan_filter != "All":
            filtered_data = filtered_data[filtered_data['Kecamatan'] == kecamatan_filter]

        st.write(f"Data yang difilter berdasarkan Tahun: {tahun_filter}, Kategori: {kategori_filter}, Kecamatan: {kecamatan_filter}")
        st.dataframe(filtered_data, use_container_width=True)

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
    else:
        st.error("Tidak ada data yang berhasil dimuat!")

except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")

# Perhitungan Total Bencana per Tahun
if not filtered_data.empty:
    filtered_data['Total'] = filtered_data.iloc[:, 3:].sum(axis=1)
    total_semua_tahun = filtered_data['Total'].sum()

    # Menampilkan total keseluruhan sebagai card
    st.metric(label="Total Keseluruhan Bencana", value=f"{total_semua_tahun}")

    grouped_by_tahun = filtered_data.groupby('Tahun', as_index=False)['Total'].sum()

    # Menampilkan chart Total Bencana per Tahun
    st.title("Total Bencana per Tahun")
    st.write(f"Data yang difilter berdasarkan Tahun: {tahun_filter}, Kategori: {kategori_filter}, Kecamatan: {kecamatan_filter}")

    chart_tahun = alt.Chart(grouped_by_tahun).mark_bar().encode(
        x=alt.X('Tahun:N', title='Tahun'),
        y=alt.Y('Total:Q', title='Total Bencana'),
        color='Tahun:N',
        tooltip=['Tahun', 'Total']  # Menampilkan tooltip ketika di-hover
    ).properties(
        width=600,
        height=400
    )

    st.altair_chart(chart_tahun, use_container_width=True)

# Pengolahan data lebih lanjut menggunakan filtered_data untuk total per bulan
if not filtered_data.empty:
    bulan = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Juni', 'Jul', 'Agt', 'Sept', 'Okt', 'Nop', 'Des']
    total_per_bulan = {bulan_name: filtered_data[bulan_name].sum() for bulan_name in bulan}

    # Menampilkan hasil dalam card
    st.title("Total Bencana per Bulan")

    st.write(f"Data yang difilter berdasarkan Tahun: {tahun_filter}, Kategori: {kategori_filter}, Kecamatan: {kecamatan_filter}")

    # Membuat bar chart dengan Altair
    chart_data = pd.DataFrame(list(total_per_bulan.items()), columns=['Bulan', 'Total'])

    chart_bulan = alt.Chart(chart_data).mark_bar().encode(
        x='Bulan:N',
        y='Total:Q',
        color='Bulan:N',
        tooltip=['Bulan', 'Total']  # Menampilkan tooltip ketika di-hover
    ).properties(
        width=600,
        height=400
    )

    st.altair_chart(chart_bulan, use_container_width=True)

# Perhitungan Total Bencana per Kategori
if not filtered_data.empty:
    grouped_by_kategori = filtered_data.groupby('Kategori', as_index=False)['Total'].sum()

    # Menampilkan chart Total Bencana per Kategori
    st.title("Total Bencana per Kategori")
    st.write(f"Data yang difilter berdasarkan Tahun: {tahun_filter}, Kategori: {kategori_filter}, Kecamatan: {kecamatan_filter}")

    chart_kategori = alt.Chart(grouped_by_kategori).mark_bar().encode(
        x=alt.X('Kategori:N', title='Kategori'),
        y=alt.Y('Total:Q', title='Total Bencana'),
        color='Kategori:N',
        tooltip=['Kategori', 'Total']  # Menampilkan tooltip ketika di-hover
    ).properties(
        width=600,
        height=400
    )

    st.altair_chart(chart_kategori, use_container_width=True)

   
# Perhitungan Total Bencana per Kecamatan
if not filtered_data.empty:
    grouped_by_kecamatan = filtered_data.groupby('Kecamatan', as_index=False)['Total'].sum()

    # Menampilkan chart Total Bencana per Kecamatan
    st.title("Total Bencana per Kecamatan")
    st.write(f"Data yang difilter berdasarkan Tahun: {tahun_filter}, Kategori: {kategori_filter}, Kecamatan: {kecamatan_filter}")

    chart_kecamatan = alt.Chart(grouped_by_kecamatan).mark_bar().encode(
        x=alt.X('Kecamatan:N', title='Kecamatan'),
        y=alt.Y('Total:Q', title='Total Bencana'),
        color='Kecamatan:N',
        tooltip=['Kecamatan', 'Total']  # Menampilkan tooltip ketika di-hover
    ).properties(
        width=600,
        height=400
    )

    st.altair_chart(chart_kecamatan, use_container_width=True)