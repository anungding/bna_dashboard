import pandas as pd
import streamlit as st

class KesehatanController:
    def __init__(self):
        # Menyiapkan data paths per tahun
        self.data_files = {
            2023: "dataset/kesehatan/tenaga_kesehatan_per_kecamatan_2023.csv",
            2022: "dataset/kesehatan/tenaga_kesehatan_per_kecamatan_2022.csv",
            2021: "dataset/kesehatan/tenaga_kesehatan_per_kecamatan_2021.csv",
            2020: "dataset/kesehatan/tenaga_kesehatan_per_kecamatan_2020.csv",
            2019: "dataset/kesehatan/tenaga_kesehatan_per_kecamatan_2019.csv",
            2018: "dataset/kesehatan/tenaga_kesehatan_per_kecamatan_2018.csv"
        }

    def load_data(self, file_path, tahun):
        # Fungsi untuk membaca dan membersihkan data per tahun
        df = pd.read_csv(file_path, sep=";")
        df['Tahun'] = str(tahun)  # Tambahkan kolom tahun
        
        # Normalisasi nama kecamatan
        df['Kecamatan'] = df['Kecamatan'].replace("Pwj Klampok", "Purwareja Klampok")
        
        # Urutkan kolom
        col_order = ['Kecamatan', 'Tahun'] + [col for col in df.columns if col not in ['Kecamatan', 'Tahun']]
        df = df[[col for col in col_order if col in df.columns]]  
        
        return df

    def get_combined_data(self):
        # Mengecek apakah data sudah dimuat di session state
        if 'df_combined' not in st.session_state:
            # Load semua data dari tahun 2018-2023
            data_list = [self.load_data(path, tahun) for tahun, path in self.data_files.items()]
            df_combined = pd.concat(data_list, ignore_index=True)

            # Normalisasi nama kolom ke format snake_case
            df_combined.columns = (
                df_combined.columns.str.strip()
                                  .str.lower()
                                  .str.replace(" ", "_")
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
            
            # Simpan ke session state
            st.session_state['df_combined'] = df_combined
        else:
            df_combined = st.session_state['df_combined']

        return df_combined

    def filter_data(self, df_combined, selected_year, selected_kecamatan):
        # Filter berdasarkan tahun dan kecamatan
        if selected_kecamatan != 'Semua Kecamatan':
            df_combined = df_combined[df_combined['kecamatan'] == selected_kecamatan]
        if selected_year != 'Semua Tahun':
            df_combined = df_combined[df_combined['tahun'] == selected_year]
        return df_combined

    def group_by_year(self, df_combined):
        # Group by tahun dan jumlahkan nilai
        return df_combined.drop(columns=['kecamatan']).groupby('tahun', as_index=False).sum()

    def group_by_kecamatan(self, df_combined):
        # Group by kecamatan dan jumlahkan nilai
        return df_combined.groupby('kecamatan', as_index=False).sum()

    def total_for_year(self, df_combined, tahun, kolom):
        return df_combined[df_combined['tahun'] == str(tahun)][kolom].sum()

    def total_for_last_year(self, df_combined, kolom):
        tahun_terakhir = df_combined['tahun'].max() 
        total = int(df_combined[df_combined['tahun'] == str(tahun_terakhir)][kolom].sum()) 
        return tahun_terakhir, total




