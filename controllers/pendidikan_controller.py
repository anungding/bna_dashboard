import pandas as pd

class PendidikanController:
    def __init__(self):
        self.data_files = {
            2023: "dataset/pendidikan/pendidikan_smk_2023.csv"
        }
        self.pendidikan_smk_2023 = self.load_all_data()

    def load_data(self, file_path, tahun):
        """Membaca CSV dan membersihkan data"""
        df = pd.read_csv(file_path)
        df.replace("-", 0, inplace=True)  # Mengganti '-' menjadi 0
        df["Tahun"] = tahun  # Menambahkan kolom Tahun
        return df

    def load_all_data(self):
        """Membaca semua data dan menggabungkannya dalam satu DataFrame"""
        data_list = [self.load_data(path, tahun) for tahun, path in self.data_files.items()]
        return pd.concat(data_list, ignore_index=True)

    def get_data(self):
        """Mengembalikan data yang sudah diproses"""
        return self.pendidikan_smk_2023
