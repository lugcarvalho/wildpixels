import streamlit as st
import ee 
import geemap.foliumap as geemap
import geopandas as gpd
import leafmap.foliumap as leafmap
from dataclasses import dataclass

@dataclass
class Area:
    nome: str
    caminho: str
    cor: str = "purple"
    carregada: bool = False

width = 950
height = 600

def carrega_feature():
    print("--- carrega-feature ---")
    #print(areasSelecionadas)
    print("--- saiu de carrega-feature ---")

def carrega_collection_geojson(mapa,file_path, layer_name,cor):
    print("--- entrou em carrega-collection-geojson ---", layer_name)
    width = 950
    height = 600
    layerparams = {'color': cor}
    print(layerparams)
    mapa.add_geojson(area.caminho,area.nome,default_popup=False)
    print("--- saiu de carrega-collection ---")

    
def carrega_collection_layer(mapa,file_path, layer_name,cor):
    print("--- entrou em carrega-collection-layer ---", layer_name)
    width = 950
    height = 600
    layerparams = {'color': cor}
    print(layerparams)
    ee_object = geemap.geojson_to_ee(file_path)
    mapa.addLayer(ee_object,layerparams, layer_name,True,0.9)
    #mapa.addLayerControl()
    #mapa.to_streamlit(width=width, height=height)
    print("--- saiu de carrega-collection ---")

def carrega_collection_gpd(mapa,file_path, layer_name,cor ):
    print("--- entrou em carrega-collection-gpd ---", layer_name)

    gdf = gpd.read_file(file_path)
        
    lon, lat = leafmap.gdf_centroid(gdf)

    mapa = leafmap.Map(center=(lat, lon), draw_export=False)
    mapa.add_gdf(gdf, layer_name=layer_name, fill_colors=[cor],default_popup=False)
    mapa.add_vector(file_path, layer_name=layer_name)
    mapa.zoom_to_gdf(gdf)
    mapa.to_streamlit(width=width, height=height)
    print("--- saiu de carrega-collection ---")


container = st.container()

# Customize the sidebar
logo = "https://wildpixels.dcc.ufmg.br/wp-content/uploads/2023/07/wildpixels-green-1.png"
st.sidebar.image(logo)

markdown = """
<https://wildpixels.dcc.ufmg.br>
"""
#st.sidebar.title("About")
st.sidebar.info(markdown)

if 'areas' not in st.session_state:
    st.session_state.areas = (
    Area("Amazonia Legal","assets/complementares/amazonia-legal.geojson","yellow",True)
    , Area("UF", "assets/complementares/UFs.geojson","brown",True)
    , Area('AC1',"https://raw.githubusercontent.com/lucascsfaria/amazonwildroadsdataset/main/geojson_line/AC1.geojson", "red",False)
    , Area('AC2',"https://raw.githubusercontent.com/lucascsfaria/amazonwildroadsdataset/main/geojson_line/AC2.geojson", "red",False)
    , Area("AM1","assets/estradas-rurais/AM1.geojson","blue",False)
    , Area("AM2", "assets/estradas-rurais/AM2.geojson","blue",False)
    , Area("AM3", "assets/estradas-rurais/AM3.geojson", "red",False)
    , Area("AM4","assets/estradas-rurais/AM4.geojson","blue",False)
    , Area("AM5", "assets/estradas-rurais/AM5.geojson","blue",False)
    , Area('AM6',"assets/estradas-rurais/AM6.geojson", "red",False)
    , Area("MT1","assets/estradas-rurais/MT1.geojson","blue",False)
    , Area("MT2","assets/estradas-rurais/MT2.geojson","blue",False)
    , Area("MT3","assets/estradas-rurais/MT3.geojson","blue",False)
    , Area("RR1", "assets/estradas-rurais/RR1.geojson","blue",False)
    , Area("RR2","assets/estradas-rurais/RR2.geojson","blue",False)
    , Area("RO1","assets/estradas-rurais/RO1.geojson", "red",False)
    , Area("TO1", "assets/estradas-rurais/TO1.geojson","blue",False)
    , Area("PA1","assets/estradas-rurais/PA1.geojson", "blue",False)
    , Area("PA2", "assets/estradas-rurais/PA2.geojson", "red",False)
    , Area("PA3", "assets/estradas-rurais/PA3.geojson","blue",False)
    , Area("PA4","assets/estradas-rurais/PA4.geojson", "blue",False)
    , Area("PA5","assets/estradas-rurais/PA5.geojson", "blue",False)
    , Area("PA6","assets/estradas-rurais/PA6.geojson", "blue",False)
    , Area("PA7", "assets/estradas-rurais/PA7.geojson", "blue",False)
    , Area("PA8","assets/estradas-rurais/PA8.geojson", "blue",False)
    , Area("PA9","assets/estradas-rurais/PA9.geojson", "red",False)
    , Area("PA10","assets/estradas-rurais/PA10.geojson","blue",False)
    , Area("PA11", "assets/estradas-rurais/PA11.geojson","blue",False)
    , Area("PA12","assets/estradas-rurais/PA12.geojson", "blue",False)
    )

areas = st.session_state.areas

options = list(geemap.basemaps.keys())
index = options.index("SATELLITE")
basemap = st.sidebar.selectbox("Select a basemap:", options, index)

st.title("Estradas rurais na Amazônia")
col1, col2 = st.columns([4, 1])

with col1:
    mapa = geemap.Map()
    mapa.add_basemap(basemap)
    contador=1
    # for area in areas:
    #     print(contador," - ", area.nome," - ", area.caminho)
    #     mapa.add_geojson(area.caminho,area.nome,default_popup=False)
    #     #area.carregada=True
    #     contador=contador+1
    #     if contador>10:
    #         break


    mapa.add_geojson("assets/complementares/amazonia-legal.geojson","Amazônia Legal")
    mapa.add_geojson("assets/complementares/UFs.geojson","UFs")
  

areasSelecionadas = []

#with col2:
    #print(areasSelecionadas)
   
#st.multiselect(label, options, default=None, format_func=special_internal_function, key=None, help=None, on_change=None, args=None, kwargs=None, *, max_selections=None, placeholder="Choose an option", disabled=False, label_visibility="visible")
#features = st.sidebar.multiselect("Selecione as áreas:", areas, None, format_func=lambda area:area.nome, key=None, help=None, on_change=carrega_feature())
features = st.sidebar.multiselect("Selecione as áreas:", areas, None, format_func=lambda area:area.nome, key=None, help=None, max_selections=18, placeholder="Selecione as áreas")
st.write('selecionadas: ', features)
for feature in features:
    areasSelecionadas.append(feature)
    
    #print(features)
    #print(areasSelecionadas)
        
with col1:
    for selecionada in areasSelecionadas:
        area = selecionada
        print(area.nome+" SELECIONADA")

        print(area)
        if area.carregada != True:
            print(area.nome+" CARREGADA")
            area.carregada=True
            mapa.add_geojson(area.caminho,area.nome)
            contador=contador+1
            if contador>10:
                break

            #carrega_collection_gpd(mapa, area.caminho, area.nome, area.cor)
            #carrega_collection_layer(mapa, area.caminho, area.nome, area.cor)
    
    mapa.setCenter(-59, -6, 5)

    mapa.to_streamlit(950,  600)












