import pandas as pd

# Fungsi untuk membaca dan membersihkan data per tahun
def load_data(file_path, tahun):
    df = pd.read_csv(file_path)

    # Mengganti nilai "-" dengan 0 di seluruh DataFrame
    df.replace("-", 0, inplace=True)

    # Menambahkan kolom Tahun untuk identifikasi
    df["Tahun"] = tahun  

    # Menampilkan DataFrame yang sudah diproses
    return df

# Load semua data dari tahun 2018-2023
data_files = {
    2023: "dataset/pendidikan/pendidikan_smk_2023.csv"
}

# Membaca dan menggabungkan data untuk setiap tahun
data_list = [load_data(path, tahun) for tahun, path in data_files.items()]

# Menggabungkan DataFrame dalam data_list menjadi satu DataFrame
df_pendidikan_smk = pd.concat(data_list, ignore_index=True)

df_pendidikan_smk
