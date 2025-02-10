import os
import pandas as pd

class TourismController:
    def __init__(self, dataset_folder='dataset/tourism/'):
        self.dataset_folder = dataset_folder
        self.data = None
        self.tahun_list = []
        self.bulan_list = []
        self.nama_wisata_list = []
        self.load_combined_data()

    def load_data_from_folder(self):
        data_files = {}
        for file_name in os.listdir(self.dataset_folder):
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
                file_path = os.path.join(self.dataset_folder, file_name)
                data_files[nama].append((file_path, int(tahun)))
        return data_files

    def preprocess_data(self, file_path, nama, tahun):
        try:
            df = pd.read_csv(file_path, sep=',')
            df.replace("-", 0, inplace=True)
            df.replace(r"^\s*-+\s*$", "0", regex=True, inplace=True)
            df.columns = df.columns.str.strip().str.lower()

            # Normalisasi nama bulan
            df['bulan'] = df['bulan'].str.strip().replace({
                "JAN": "JANUARI", "FEB": "PEBRUARI", "MAR": "MARET",
                "APR": "APRIL", "MEI": "MEI", "JUN": "JUNI",
                "JUL": "JULI", "AGS": "AGUSTUS", "SEP": "SEPTEMBER",
                "OKT": "OKTOBER", "NOP": "NOPEMBER", "DES": "DESEMBER"
            })

            # **Gabungkan semua kolom terkait kunjungan jika ada**
            kolom_kunjungan = ['kunjungan', 'pengunjung', 'jumlah kunjungan', 'total pengunjung']
            kolom_ada = [col for col in kolom_kunjungan if col in df.columns]

            if len(kolom_ada) > 1:
                df['kunjungan'] = df[kolom_ada].sum(axis=1)  # Jumlahkan semua yang ada
                df.drop(columns=kolom_ada, inplace=True)  # Hapus semua kolom lama
            elif len(kolom_ada) == 1:
                df.rename(columns={kolom_ada[0]: 'kunjungan'}, inplace=True)

            # Hapus baris dengan bulan kosong
            if 'bulan' in df.columns:
                df = df.dropna(subset=['bulan'])

            # Pastikan kolom 'kunjungan' dalam format numerik
            if 'kunjungan' in df.columns:
                df['kunjungan'] = df['kunjungan'].astype(str).str.replace(',', '').astype(float)
                df['kunjungan'] = df['kunjungan'].fillna(0)

            # Tambahkan kolom tahun dan nama
            df['tahun'] = str(tahun)
            df['nama'] = nama

            # Atur ulang urutan kolom
            col_order = ['nama', 'tahun', 'bulan'] + [col for col in df.columns if col not in ['nama', 'tahun', 'bulan']]
            df = df[[col for col in col_order if col in df.columns]]

            return df

        except Exception as e:
            print(f"Kesalahan saat memproses file {file_path}: {e}")
            return pd.DataFrame()


    def load_combined_data(self):
        data_files = self.load_data_from_folder()
        data_frames = []
        self.tahun_list, self.bulan_list, self.nama_wisata_list = set(), set(), set()

        for nama, files in data_files.items():
            for file_path, tahun in files:
                df = self.preprocess_data(file_path, nama, tahun)
                if not df.empty:
                    data_frames.append(df)
                    self.tahun_list.add(tahun)
                    self.bulan_list.update(df['bulan'].unique())
                    self.nama_wisata_list.add(nama)

        self.data = pd.concat(data_frames, ignore_index=True) if data_frames else pd.DataFrame()
        self.tahun_list = ["Semua Tahun"] + sorted(self.tahun_list)
        self.bulan_list = ["Semua Bulan"] + sorted(self.bulan_list)
        self.nama_wisata_list = ["Semua Nama Wisata"] + sorted(self.nama_wisata_list)

    def get_filtered_data(self, tahun, bulan, nama_wisata):
        df = self.data.copy()
        if tahun != "Semua Tahun":
            df = df[df['tahun'] == str(tahun)]
        if bulan != "Semua Bulan":
            df = df[df['bulan'] == bulan]
        if nama_wisata != "Semua Nama Wisata":
            df = df[df['nama'] == nama_wisata]
        return df

    def convert_df(self, df):
        """Mengonversi DataFrame ke CSV untuk diunduh."""
        return df.to_csv(index=False).encode('utf-8')

    def get_grouped_data(self, df, column):
        """Mengelompokkan data berdasarkan kolom tertentu."""
        if column in df.columns:
            return df.groupby(column, as_index=False)['kunjungan'].sum()
        return pd.DataFrame()

    def get_total_per_bulan(self, df):
        """Menghitung total kunjungan per bulan."""
        bulan_list = ["JANUARI", "PEBRUARI", "MARET", "APRIL", "MEI", "JUNI", 
                      "JULI", "AGUSTUS", "SEPTEMBER", "OKTOBER", "NOPEMBER", "DESEMBER"]
        total_per_bulan = {bulan: df[df['bulan'] == bulan]['kunjungan'].sum() for bulan in bulan_list if bulan in df['bulan'].unique()}
        return pd.DataFrame(list(total_per_bulan.items()), columns=['Bulan', 'Total'])
