import pandas as pd
import os

dataset_folder = 'dataset/bencana/'

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

def load_combined_data():
    data_files = load_data_from_folder(dataset_folder)
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
                continue

    return pd.concat(data_frames, ignore_index=True) if data_frames else pd.DataFrame()

def filter_data(df, tahun, kategori, kecamatan):
    filtered_df = df.copy()
    
    if tahun != "All":
        filtered_df = filtered_df[filtered_df['Tahun'] == tahun]
    if kategori != "All":
        filtered_df = filtered_df[filtered_df['Kategori'] == kategori]
    if kecamatan != "All":
        filtered_df = filtered_df[filtered_df['Kecamatan'] == kecamatan]

    return filtered_df

def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

def get_grouped_data(df, column):
    return df.groupby(column, as_index=False)['Total'].sum()

def get_total_per_bulan(df):
    bulan = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Juni', 'Jul', 'Agt', 'Sept', 'Okt', 'Nop', 'Des']
    total_per_bulan = {bulan_name: df[bulan_name].sum() for bulan_name in bulan if bulan_name in df.columns}
    return pd.DataFrame(list(total_per_bulan.items()), columns=['Bulan', 'Total'])
