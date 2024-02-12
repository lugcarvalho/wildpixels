import streamlit as st
from streamlit_folium import st_folium
import folium
import requests
from dataclasses import dataclass
import geemap.foliumap as geemap

@dataclass
class Area:
    nome: str
    caminho: str
    cor: str = "purple"
    carregada: bool = False


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
    Area("Amazonia Legal","https://raw.githubusercontent.com/lugcarvalho/wildpixels/master/assets/complementares/amazonia-legal.geojson","yellow",True)
    , Area("UF", "https://raw.githubusercontent.com/lugcarvalho/wildpixels/master/assets/complementares/UFs.geojsonjson","brown",True),
    Area('AC1',"https://raw.githubusercontent.com/lucascsfaria/amazonwildroadsdataset/main/geojson_line/AC1.geojson", "red",False)
    , Area('AC2',"https://raw.githubusercontent.com/lucascsfaria/amazonwildroadsdataset/main/geojson_line/AC2.geojson", "red",False)
    , Area("AM1","https://raw.githubusercontent.com/lucascsfaria/amazonwildroadsdataset/main/geojson_line/AM1.geojson","blue",False)
    , Area("AM2", "https://raw.githubusercontent.com/lucascsfaria/amazonwildroadsdataset/main/geojson_line/AM2.geojson","blue",False)
    , Area("AM3", "https://raw.githubusercontent.com/lucascsfaria/amazonwildroadsdataset/main/geojson_line/AM3.geojson", "red",False)
    , Area("AM4","https://raw.githubusercontent.com/lucascsfaria/amazonwildroadsdataset/main/geojson_line/AM4.geojson","blue",False)
    , Area("AM5", "https://raw.githubusercontent.com/lucascsfaria/amazonwildroadsdataset/main/geojson_line/AM5.geojson","blue",False)
    , Area('AM6',"https://raw.githubusercontent.com/lucascsfaria/amazonwildroadsdataset/main/geojson_line/AM6.geojson", "red",False)
    , Area("MT1","https://raw.githubusercontent.com/lucascsfaria/amazonwildroadsdataset/main/geojson_line/MT1.geojson","blue",False)
    , Area("MT2","https://raw.githubusercontent.com/lucascsfaria/amazonwildroadsdataset/main/geojson_line/MT2.geojson","blue",False)
    , Area("MT3","https://raw.githubusercontent.com/lucascsfaria/amazonwildroadsdataset/main/geojson_line/MT3.geojson","blue",False)
    , Area("RR1", "https://raw.githubusercontent.com/lucascsfaria/amazonwildroadsdataset/main/geojson_line/RR1.geojson","blue",False)
    , Area("RR2","https://raw.githubusercontent.com/lucascsfaria/amazonwildroadsdataset/main/geojson_line/RR2.geojson","blue",False)
    , Area("RO1","https://raw.githubusercontent.com/lucascsfaria/amazonwildroadsdataset/main/geojson_line/RO1.geojson", "red",False)
    , Area("TO1", "https://raw.githubusercontent.com/lucascsfaria/amazonwildroadsdataset/main/geojson_line/TO1.geojson","blue",False)
    , Area("PA1","https://raw.githubusercontent.com/lucascsfaria/amazonwildroadsdataset/main/geojson_line/PA1.geojson", "blue",False)
    , Area("PA2", "https://raw.githubusercontent.com/lucascsfaria/amazonwildroadsdataset/main/geojson_line/PA2.geojson", "red",False)
    , Area("PA3", "https://raw.githubusercontent.com/lucascsfaria/amazonwildroadsdataset/main/geojson_line/PA3.geojson","blue",False)
    , Area("PA4","https://raw.githubusercontent.com/lucascsfaria/amazonwildroadsdataset/main/geojson_line/PA4.geojson", "blue",False)
    , Area("PA5","https://raw.githubusercontent.com/lucascsfaria/amazonwildroadsdataset/main/geojson_line/PA5.geojson", "blue",False)
    , Area("PA6","https://raw.githubusercontent.com/lucascsfaria/amazonwildroadsdataset/main/geojson_line/PA6.geojson", "blue",False)
    , Area("PA7", "https://raw.githubusercontent.com/lucascsfaria/amazonwildroadsdataset/main/geojson_line/PA7.geojson", "blue",False)
    , Area("PA8","https://raw.githubusercontent.com/lucascsfaria/amazonwildroadsdataset/main/geojson_line/PA8.geojson", "blue",False)
    , Area("PA9","https://raw.githubusercontent.com/lucascsfaria/amazonwildroadsdataset/main/geojson_line/PA9.geojson", "red",False)
    , Area("PA10","https://raw.githubusercontent.com/lucascsfaria/amazonwildroadsdataset/main/geojson_line/PA10.geojson","blue",False)
    , Area("PA11", "https://raw.githubusercontent.com/lucascsfaria/amazonwildroadsdataset/main/geojson_line/PA11.geojson","blue",False)
    , Area("PA12","https://raw.githubusercontent.com/lugcarvalho/wildpixels/master/https://raw.githubusercontent.com/lucascsfaria/amazonwildroadsdataset/main/geojson_line/PA12.geojson", "blue",False)
    )

areas = st.session_state.areas


def app():
    areasSelecionadas = []
    areasCarregadas = []

    options = list(geemap.basemaps.keys())
    index = options.index("SATELLITE")
    basemap = st.sidebar.selectbox("Select a basemap:", options, index)

    features = st.sidebar.multiselect("Selecione as áreas:", areas, None, format_func=lambda area:area.nome, key=None, help=None, max_selections=18, placeholder="Selecione as áreas")
    st.write('selecionadas: ', features)
    for feature in features:
        areasSelecionadas.append(feature)

    st.title("Estradas rurais na Amazônia")

    m = folium.Map([-6,-62], zoom_start=5,width=900)

    if len(areasSelecionadas) > 0:
        for selecionada in areasSelecionadas:
            area = selecionada
            print(area.nome+" SELECIONADA")
            print(area)
            if area.carregada != True:
                print(area.nome+" CARREGADA")
                area.carregada=True
                areasCarregadas.append(area)
                folium.Choropleth(area.caminho, line_color=area.cor, name=area.nome).add_to(m)

        
    areasSelecionadas = areasCarregadas  
    print("saiu do for")
    folium.LayerControl().add_to(m)
    st_data = st_folium(m,width=900)
    exit()

app()