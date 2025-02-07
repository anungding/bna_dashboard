import streamlit as st
import json
import folium
import pandas as pd
import branca
from streamlit_folium import st_folium

# Fungsi untuk membaca dan membersihkan file CSV
def load_csv(file_path):
    """
    Membaca CSV, membersihkan data, mengganti nilai "-" menjadi 0, dan mengonversi kolom numerik.
    """
    df = pd.read_csv(file_path)
    
    # Bersihkan kolom kecamatan: menghapus spasi dan mengubah nama yang tidak sesuai
    df['kecamatan'] = df['kecamatan'].str.replace(" ", "") 
    df['kecamatan'] = df['kecamatan'].str.replace("PurwarejaKlampok", "Purworeja Klampok")
    
    # Ganti tanda "-" dengan 0 agar bisa dikonversi ke angka
    df.replace("-", 0, inplace=True)
    
    # Mengonversi semua kolom selain 'kecamatan' ke float
    for column in df.columns:
        if column != "kecamatan":
            df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)  # Ganti nilai yang tidak bisa dikonversi dengan 0
    
    return df

# Path ke file GeoJSON
geojson_file_path = "dataset/geojson/BNAGEOJSON.geojson"

# Pilihan dataset
dataset_option = st.selectbox(
    "Pilih Dataset",
    ["Penduduk-BPS-2019", "Pertanian-Sawah-BPS-2023"]
)

# Menentukan warna berdasarkan dataset yang dipilih
color_mapping = {
    "Penduduk-BPS-2019": "Reds_09",  # Skema warna merah untuk penduduk
    "Pertanian-Sawah-BPS-2023": "Greens_09"  # Skema warna hijau untuk pertanian
}

# Menentukan file CSV berdasarkan pilihan
dataset_file_mapping = {
    "Penduduk-BPS-2019": "dataset/penduduk/penduduk_bna_2019.csv",
    "Pertanian-Sawah-BPS-2023": "dataset/pertanian/pertanian_sawah_2023.csv"
}

csv_file_path = dataset_file_mapping.get(dataset_option)

# Membaca GeoJSON
with open(geojson_file_path, "r", encoding="utf-8") as geojson_file:
    geojson_data = json.load(geojson_file)

# Membaca data CSV sesuai pilihan
data_csv = load_csv(csv_file_path)

# Menentukan kolom total (kolom terakhir)
total_column_name = data_csv.columns[-1]

# Menambahkan data CSV ke GeoJSON
for feature in geojson_data['features']:
    kecamatan_name = feature['properties']['WADMKC']
    
    # Menambahkan nilai data CSV ke properti GeoJSON
    total_value = data_csv[data_csv['kecamatan'] == kecamatan_name][total_column_name].values
    if total_value.size > 0:
        feature['properties']['Total'] = float(total_value[0])  # Gunakan float untuk menangani desimal
    else:
        feature['properties']['Total'] = 0

    # Menambahkan data tambahan jika kolom tersedia
    for column in data_csv.columns:
        if column != 'kecamatan' and column != total_column_name:
            feature['properties'][column] = float(data_csv[data_csv['kecamatan'] == kecamatan_name][column].values[0])

# Menentukan nilai minimum dan maksimum dari total
min_total = data_csv[total_column_name].min()
max_total = data_csv[total_column_name].max()

# Pilih warna berdasarkan dataset
selected_color = color_mapping.get(dataset_option, "Reds_09")  # Default menggunakan skema warna merah

# Fungsi untuk menentukan warna berdasarkan data CSV
def get_color_based_on_data(feature):
    """
    Fungsi untuk menentukan warna berdasarkan nilai total dalam data CSV.
    """
    value = feature["properties"].get("Total", 0)
    colormap = branca.colormap.linear.__getattribute__(selected_color).scale(min_total, max_total)  # Gunakan skema warna yang sesuai
    return colormap(value)

# Inisialisasi peta
map_center = [-7.3652570633814445, 109.652297639757]  # Titik tengah peta
map_zoom = 11  # Level zoom peta
tile_layer = "CartoDB positron"  # Layer peta
folium_map = folium.Map(location=map_center, zoom_start=map_zoom, tiles=tile_layer)

# Membangun tooltip dinamis
tooltip_fields = ["WADMKC", "Total"]
tooltip_aliases = ["Kecamatan:", "Total:"]

# Menambahkan kolom tambahan ke tooltip jika ada
for column in data_csv.columns:
    if column != 'kecamatan' and column != total_column_name:
        tooltip_fields.append(column)
        tooltip_aliases.append(f"{column.capitalize()}:")

# Menambahkan GeoJSON ke peta dengan style dan tooltip
folium.GeoJson(
    geojson_data,
    style_function=lambda feature: {
        'fillColor': get_color_based_on_data(feature),
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.6
    },
    tooltip=folium.GeoJsonTooltip(
        fields=tooltip_fields,
        aliases=tooltip_aliases,
        localize=True
    )
).add_to(folium_map)

# Menampilkan peta di Streamlit
st_folium(folium_map, width="100%", height=600)

# Menampilkan data untuk verifikasi
st.write(data_csv)
