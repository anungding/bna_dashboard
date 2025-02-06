import streamlit as st
import pandas as pd

st.title("DATA KESEHATAN BNA")

# ---------------- TENAGA KESEHATAN ----------------
st.markdown(
    """
    ### 🧑‍⚕️DATA TENAGA KESEHATAN BNA🧑‍⚕️
    Dataset diambil dari: -
    
    Periode: 2018-2023
    """
)

# Fungsi untuk membaca dan membersihkan data per tahun
def load_data(file_path, tahun):
    df = pd.read_csv(file_path, sep=";")
    df['Tahun'] = str(tahun)  # Tambahkan kolom tahun
    
    # Normalisasi nama kecamatan (contoh: mengganti "Pwj Klampok" menjadi "Purwareja Klampok")
    df['Kecamatan'] = df['Kecamatan'].replace("Pwj Klampok", "Purwareja Klampok")
    
    # Urutkan kolom agar "Kecamatan" dan "Tahun" selalu di awal
    col_order = ['Kecamatan', 'Tahun'] + [col for col in df.columns if col not in ['Kecamatan', 'Tahun']]
    df = df[[col for col in col_order if col in df.columns]]  
    
    return df

# Load semua data dari tahun 2018-2023
data_files = {
    2023: "dataset/kesehatan/tenaga_kesehatan_per_kecamatan_2023.csv",
    2022: "dataset/kesehatan/tenaga_kesehatan_per_kecamatan_2022.csv",
    2021: "dataset/kesehatan/tenaga_kesehatan_per_kecamatan_2021.csv",
    2020: "dataset/kesehatan/tenaga_kesehatan_per_kecamatan_2020.csv",
    2019: "dataset/kesehatan/tenaga_kesehatan_per_kecamatan_2019.csv",
    2018: "dataset/kesehatan/tenaga_kesehatan_per_kecamatan_2018.csv"
}

data_list = [load_data(path, tahun) for tahun, path in data_files.items()]

# Gabungkan semua data menjadi satu DataFrame
df_combined = pd.concat(data_list, ignore_index=True)

# Normalisasi nama kolom ke format snake_case (huruf kecil, tanpa spasi, pakai underscore)
df_combined.columns = (
    df_combined.columns.str.strip()      # Hapus spasi di awal & akhir
                      .str.lower()      # Ubah huruf jadi kecil semua
                      .str.replace(" ", "_")  # Ganti spasi dengan underscore
)

# Gabungkan kolom yang memiliki makna sama
kolom_duplikat = {
    'tenaga_kesehatan_masyarakat': 'kesmas',
    'tenaga_kesehatan_lingkungan': 'kesling',
    'ahli_gizi': 'ahli__gizi',
    'tenaga_gizi': 'ahli_gizi',
    'ahli_teknologi_laboratorium_medik': 'atlm'
}

for kolom_target, kolom_dupe in kolom_duplikat.items():
    if kolom_target in df_combined.columns and kolom_dupe in df_combined.columns:
        df_combined[kolom_target] = df_combined[kolom_target].fillna(0) + df_combined[kolom_dupe].fillna(0)
        df_combined = df_combined.drop(columns=[kolom_dupe])  # Hapus kolom duplikat

# Ganti semua nilai NaN atau None dengan 0
df_combined = df_combined.fillna(0)


# Tampilkan hasil akhir
st.dataframe(df_combined)

# CARD

if not df_combined.empty:

    st.markdown(
        """
        ##### Jumlah Tenaga Kesehatan *update 2023
        """
    )
    
    total_dokter_2023 = df_combined[df_combined['tahun'] == "2023"]['dokter'].sum()
    total_perawat_2023 = df_combined[df_combined['tahun'] == "2023"]['perawat'].sum()
    total_bidan_2023 = df_combined[df_combined['tahun'] == "2023"]['bidan'].sum()
    total_farmasi_2023 = df_combined[df_combined['tahun'] == "2023"]['farmasi'].sum()
    total_tenaga_gizi_2023 = df_combined[df_combined['tahun'] == "2023"]['tenaga_gizi'].sum()
    total_dokter_gigi_2023 = df_combined[df_combined['tahun'] == "2023"]['dokter_gigi'].sum()
   
    # Menampilkan tiga metric (card)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Jumlah Dokter", value=f"{int(total_dokter_2023)}")

    with col2:
        st.metric(label="Jumlah Perawat", value=f"{int(total_perawat_2023)}")

    with col3:
        st.metric(label="Jumlah Bidan", value=f"{int(total_bidan_2023)}")

    col4, col5, col6 = st.columns(3)

    with col4:
        st.metric(label="Jumlah Dokter Gigi", value=f"{int(total_dokter_gigi_2023)}")

    with col5:
        st.metric(label="Jumlah Tenaga Farmasi", value=f"{int(total_farmasi_2023)}")

    with col6:
        st.metric(label="Jumlah Tenaga Gizi", value=f"{int(total_tenaga_gizi_2023)}")

group_by_year = df_combined.drop(columns=['kecamatan']).groupby('tahun',  as_index=False).sum()

st.markdown(
    """
    ##### DATA JUMLAH TENAGA KESEHATAN DARI TAHUN KE TAHUN
    ###### *tahun 2018-2023
    """
)
group_by_year

group_by_kecamatan = df_combined[df_combined['tahun'] == "2023"].groupby('kecamatan',  as_index=False).sum()

st.markdown(
    """
    ##### DATA JUMLAH TENAGA KESEHATAN DARI TAHUN KE TAHUN
    ###### *tahun 2023
    """
)
group_by_kecamatan
