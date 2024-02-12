import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd
import pandas as pd
import os




st.title("WildRoadsMap")

list_geojson = os.listdir("./assets/estradas-rurais/")
print(list_geojson)

#gdf = gpd.read_file("./final_results/resultnull_AC1.geojson")
gdf = gpd.GeoDataFrame()
for geojson in list_geojson:
    gdf_aux = gpd.read_file("./assets/estradas-rurais/"+geojson)
    gdf = pd.concat([gdf,gdf_aux])

lon, lat = leafmap.gdf_centroid(gdf)

m = leafmap.Map(center=(lat, lon), draw_export=True)
m.add_gdf(gdf, layer_name="RoadWildMap")
#in_geojson = 'https://raw.githubusercontent.com/opengeos/leafmap/master/examples/data/cable_geo.geojson'
#m.add_geojson(in_geojson, layer_name="Cable lines")

m.to_streamlit(950,  600)