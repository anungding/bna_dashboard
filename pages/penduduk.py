import streamlit as st
import json
from shapely.geometry import shape
import folium
from streamlit_folium import st_folium
import pandas as pd
import branca
from folium.plugins import MarkerCluster
from folium.features import DivIcon
from folium.plugins import FloatImage

st.title("DATA PENDUDUK BNA")

# ====== Load GeoJSON Data ======
geojson_file_path = "dataset/geojson/BNAGEOJSON.geojson"
with open(geojson_file_path, "r", encoding="utf-8") as geojson_file:
    geojson_data = json.load(geojson_file)

# ====== Load Population Data ======
population_csv_path = 'dataset/penduduk/penduduk_bna_2019.csv'
penduduk_data = pd.read_csv(population_csv_path)

# Normalisasi nama kecamatan (hapus spasi & perbaiki kesalahan nama)
penduduk_data['kecamatan'] = penduduk_data['kecamatan'].str.replace(" ", "")
penduduk_data['kecamatan'] = penduduk_data['kecamatan'].str.replace("PurwarejaKlampok", "Purworeja Klampok")

# Hitung total populasi
penduduk_data['populasi'] = penduduk_data['laki_laki'] + penduduk_data['perempuan']
population_df = pd.DataFrame(penduduk_data)
population_df['populasi'] = population_df['populasi'].astype(int)

# Tambahkan data populasi ke GeoJSON
for feature in geojson_data['features']:
    kecamatan_name = feature['properties']['WADMKC']  
    population = population_df[population_df['kecamatan'] == kecamatan_name]['populasi'].values
    laki_laki = population_df[population_df['kecamatan'] == kecamatan_name]['laki_laki'].values
    perempuan = population_df[population_df['kecamatan'] == kecamatan_name]['perempuan'].values
    
    feature['properties']['POPULASI'] = int(population[0]) if population.size > 0 else 0
    feature['properties']['Laki-Laki'] = int(laki_laki[0]) if laki_laki.size > 0 else 0
    feature['properties']['Perempuan'] = int(perempuan[0]) if perempuan.size > 0 else 0

# ====== Fungsi Pewarnaan Berdasarkan Populasi ======
def get_population_color(feature):
    population = feature["properties"].get("POPULASI", 0)
    colormap = branca.colormap.linear.Reds_09.scale(0, 150000)
    return colormap(population)

# ====== Inisialisasi Peta ======
map_center = [-7.3652570633814445, 109.652297639757]
map_zoom = 11
tile_layer = "CartoDB positron"
folium_map = folium.Map(location=map_center, zoom_start=map_zoom, tiles=tile_layer)

# ====== Tambahkan GeoJSON ke Peta ======
folium.GeoJson(
    geojson_data,
    style_function=lambda feature: {
        'fillColor': get_population_color(feature),
        'color': 'black',
        'weight': 2,  # Batas tepi lebih tebal agar lebih responsif
        'fillOpacity': 0.6
    },
    tooltip=folium.GeoJsonTooltip(
        fields=["WADMKC", "POPULASI", "Laki-Laki", "Perempuan"],
        aliases=["Kecamatan:", "Total Populasi:", "Laki-laki:", "Perempuan:"],
        localize=True
    ),
    popup=folium.GeoJsonPopup(
        fields=["WADMKC", "POPULASI", "Laki-Laki", "Perempuan"],
        aliases=["Kecamatan:", "Total Populasi:", "Laki-laki:", "Perempuan:"]
    )
).add_to(folium_map)

# ====== Tambahkan Statistik Populasi ======
total_jumlah_penduduk = population_df['populasi'].sum()
total_jumlah_laki_laki = population_df['laki_laki'].sum()
total_jumlah_perempuan = population_df['perempuan'].sum()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("TOTAL PENDUDUK", total_jumlah_penduduk)
with col2:
    st.metric("JUMLAH LAKI-LAKI", total_jumlah_laki_laki)
with col3:
    st.metric("JUMLAH PEREMPUAN", total_jumlah_perempuan)

# ====== Tampilkan Peta ======
st.markdown("""
#### PETA SEBARAN JUMLAH PENDUDUK BNA BERDASARKAN JENIS KELAMIN
*Arahkan kursor pada peta untuk melihat detail sebaran
""")
st_folium(folium_map, width="100%", height=600)

# ====== Tambahkan Sumber Data ======
st.markdown("Sumber: BPS KAB. BANJARNEGARA 2019")
