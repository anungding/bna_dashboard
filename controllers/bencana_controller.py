import pandas as pd
import os
import streamlit as st

class BencanaController:
    def __init__(self, dataset_folder='dataset/bencana/'):
        self.dataset_folder = dataset_folder
        self.data = None
        self.load_combined_data()

    def load_data_from_folder(self):
        """Membaca semua file CSV di folder dataset dan mengelompokkannya berdasarkan kategori dan tahun."""
        data_files = {}
        for file_name in os.listdir(self.dataset_folder):
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
                file_path = os.path.join(self.dataset_folder, file_name)
                data_files[kategori].append((file_path, int(tahun)))

        return data_files

    def load_combined_data(self):
        """Menggabungkan semua dataset bencana dalam satu DataFrame."""
        if "bencana_data" in st.session_state:
            self.data = st.session_state["bencana_data"]
            return self.data

        data_files = self.load_data_from_folder()
        data_frames = []

        for kategori, files in data_files.items():
            for file_path, tahun in files:
                try:
                    df = pd.read_csv(file_path, sep=';')
                    df.columns = df.columns.str.strip()
                    df.replace("-", 0, inplace=True)
                    df['Tahun'] = str(tahun)
                    df['Kategori'] = kategori

                    # Urutan kolom yang lebih rapi
                    col_order = ['Kecamatan', 'Kategori', 'Tahun'] + [col for col in df.columns if col not in ['Kecamatan', 'Kategori', 'Tahun']]
                    df = df[col_order]

                    # Konversi data ke numerik
                    for col in df.columns:
                        if col not in ['Kecamatan', 'Kategori', 'Tahun']:
                            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

                    # Tambahkan kolom total bencana per baris
                    df['Total'] = df.iloc[:, 3:].sum(axis=1)

                    data_frames.append(df)
                except FileNotFoundError:
                    continue

        combined_df = pd.concat(data_frames, ignore_index=True) if data_frames else pd.DataFrame()
        st.session_state["bencana_data"] = combined_df  # Simpan ke session state
        self.data = combined_df
        return self.data

    def filter_data(self, tahun="All", kategori="All", kecamatan="All"):
        """Filter data berdasarkan tahun, kategori, dan kecamatan."""
        if self.data is None or self.data.empty:
            return pd.DataFrame()

        filtered_df = self.data.copy()

        if tahun != "All":
            filtered_df = filtered_df[filtered_df['Tahun'] == tahun]
        if kategori != "All":
            filtered_df = filtered_df[filtered_df['Kategori'] == kategori]
        if kecamatan != "All":
            filtered_df = filtered_df[filtered_df['Kecamatan'] == kecamatan]

        return filtered_df

    def convert_df(self, df):
        """Mengonversi DataFrame ke CSV untuk diunduh."""
        return df.to_csv(index=False).encode('utf-8')

    def get_grouped_data(self, df, column):
        """Mengelompokkan data berdasarkan kolom tertentu."""
        return df.groupby(column, as_index=False)['Total'].sum()

    def get_total_per_bulan(self, df):
        """Menghitung total bencana per bulan."""
        bulan = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Juni', 'Jul', 'Agt', 'Sept', 'Okt', 'Nop', 'Des']
        total_per_bulan = {bulan_name: df[bulan_name].sum() for bulan_name in bulan if bulan_name in df.columns}
        return pd.DataFrame(list(total_per_bulan.items()), columns=['Bulan', 'Total'])


