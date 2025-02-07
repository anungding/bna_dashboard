import os
import pandas as pd

# Load data
dataset_folder = 'dataset/pariwisata/'

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

def preprocess_data(file_path, nama, tahun):
    try:
        df = pd.read_csv(file_path, sep=',')
        df.replace("-", 0, inplace=True)
        df.replace(r"^\s*-+\s*$", "0", regex=True, inplace=True)
        df.columns = df.columns.str.strip().str.lower()

        df['bulan'] = df['bulan'].str.strip().replace({
            "JAN": "JANUARI", "FEB": "PEBRUARI", "MAR": "MARET",
            "APR": "APRIL", "MEI": "MEI", "JUN": "JUNI",
            "JUL": "JULI", "AGS": "AGUSTUS", "SEP": "SEPTEMBER",
            "OKT": "OKTOBER", "NOP": "NOPEMBER", "DES": "DESEMBER"
        })

        df = df.rename(columns={'pengunjung': 'kunjungan'})

        if 'kunjungan' in df.columns and 'pengunjung' in df.columns:
            df['kunjungan'] = df[['kunjungan', 'pengunjung']].sum(axis=1)
            df.drop(columns=['pengunjung'], inplace=True)
        
        if 'bulan' in df.columns:
            df = df.dropna(subset=['bulan'])

        if 'kunjungan' in df.columns:
            df['kunjungan'] = df['kunjungan'].astype(str).str.replace(',', '').astype(float)
            df['kunjungan'] = df['kunjungan'].fillna(0)

        df['tahun'] = str(tahun)
        df['nama'] = nama

        col_order = ['nama', 'tahun', 'bulan'] + [col for col in df.columns if col not in ['nama', 'tahun', 'bulan']]
        df = df[[col for col in col_order if col in df.columns]]  

        return df

    except Exception as e:
        print(f"Kesalahan saat memproses file {file_path}: {e}")
        return pd.DataFrame()

def load_and_combine_data():
    data_files = load_data_from_folder(dataset_folder)
    data_frames = []
    tahun_list, bulan_list, nama_wisata_list = set(), set(), set()

    for nama, files in data_files.items():
        for file_path, tahun in files:
            df = preprocess_data(file_path, nama, tahun)
            if not df.empty:
                data_frames.append(df)
                tahun_list.add(tahun)
                bulan_list.update(df['bulan'].unique())
                nama_wisata_list.add(nama)

    df_combined = pd.concat(data_frames, ignore_index=True) if data_frames else pd.DataFrame()
    tahun_list = ["All"] + sorted(tahun_list)
    bulan_list = ["All"] + sorted(bulan_list)
    nama_wisata_list = ["All"] + sorted(nama_wisata_list)

    return df_combined, tahun_list, bulan_list, nama_wisata_list
def get_filtered_data(df, tahun, bulan, nama_wisata):
    """Memfilter data berdasarkan pilihan pengguna."""
    if tahun != "All":
        df = df[df['tahun'] == str(tahun)]
    if bulan != "All":
        df = df[df['bulan'] == bulan]
    if nama_wisata != "All":
        df = df[df['nama'] == nama_wisata]
    return df