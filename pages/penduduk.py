import streamlit as st
import json
from shapely.geometry import shape
import folium
from streamlit_folium import st_folium
import pandas as pd
import branca
from folium import Marker
from folium.plugins import MarkerCluster

st.title("DATA PENDUDUK BNA")

st.markdown(
"""
##### Data belum ditampilkan...
"""
)
geojson_file_path = "dataset/geojson/BNAGEOJSON.geojson"
with open(geojson_file_path, "r", encoding="utf-8") as geojson_file:
    geojson_data = json.load(geojson_file)


population_csv_path = 'dataset/penduduk/penduduk_bna_2019.csv'
penduduk_data = pd.read_csv(population_csv_path)


penduduk_data['kecamatan'] = penduduk_data['kecamatan'].str.replace(" ", "") 
penduduk_data['kecamatan'] = penduduk_data['kecamatan'].str.replace("PurwarejaKlampok", "Purworeja Klampok") 

penduduk_data['populasi'] = penduduk_data['laki_laki'] + penduduk_data['perempuan']

population_df = pd.DataFrame(penduduk_data)

population_df['populasi'] = population_df['populasi'].astype(int)

for feature in geojson_data['features']:
    kecamatan_name = feature['properties']['WADMKC'] 

    population = population_df[population_df['kecamatan'] == kecamatan_name]['populasi'].values
    laki_laki = population_df[population_df['kecamatan'] == kecamatan_name]['laki_laki'].values
    perempuan = population_df[population_df['kecamatan'] == kecamatan_name]['perempuan'].values
    
   
    if population.size > 0:
        feature['properties']['POPULASI'] = int(population[0])
    else:
        feature['properties']['POPULASI'] = 0 

    if laki_laki.size > 0 and perempuan.size > 0:
        feature['properties']['Laki-Laki'] = int(laki_laki[0])
        feature['properties']['Perempuan'] = int(perempuan[0])
    else:
        feature['properties']['Laki-Laki'] = 0
        feature['properties']['Perempuan'] = 0


def get_population_color(feature):
    population = feature["properties"].get("POPULASI", 0)  
    colormap = branca.colormap.linear.Reds_09.scale(0, 150000)
    return colormap(population)  

map_center = [-7.3652570633814445, 109.652297639757] 
map_zoom = 11 
tile_layer = "CartoDB positron" 


folium_map = folium.Map(location=map_center, zoom_start=map_zoom, tiles=tile_layer)


folium.GeoJson(
    geojson_data,
    style_function=lambda feature: {
        'fillColor': get_population_color(feature),
        'color': 'black',  
        'weight': 1, 
        'fillOpacity': 0.6 
    },
    tooltip=folium.GeoJsonTooltip(
        fields=["WADMKC", "POPULASI", "Laki-Laki", "Perempuan"], 
        aliases=["Kecamatan:", "Total Populasi:", "Laki-laki:", "Perempuan:"],
        localize=True
    )
).add_to(folium_map)


for feature in geojson_data['features']:
    kecamatan_name = feature['properties']['WADMKC']
    geometry = shape(feature['geometry']) 
    centroid = geometry.centroid 
    
    
    latitude = centroid.y
    longitude = centroid.x
    
    
    folium.Marker(
        location=[latitude, longitude],
        popup=f"Kecamatan: {kecamatan_name}\nPopulasi: {feature['properties']['POPULASI']}\nLaki-laki: {feature['properties']['Laki-Laki']}\nPerempuan: {feature['properties']['Perempuan']}",
        icon=folium.Icon(icon="cloud", color="blue")
    ).add_to(folium_map)


total_jumlah_penduduk = population_df['populasi'].sum()
total_jumlah_laki_laki = population_df['laki_laki'].sum()
total_jumlah_perempuan = population_df['perempuan'].sum()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("JUMLAH PEREMPUAN", total_jumlah_penduduk)
with col2:
    st.metric("JUMLAH LAKI-LAKI", total_jumlah_laki_laki)
with col3:
    st.metric("JUMLAH PEREMPUAN", total_jumlah_perempuan)

st.markdown(
    """
        Sumber: BPS KAB. BANJARNEGARA 2019
    """
)
st_folium(folium_map, width="100%", height=600)
