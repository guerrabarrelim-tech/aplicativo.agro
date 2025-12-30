import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import Draw

# Configuração da página
st.set_page_config(page_title="Gestor de Safra Pro", layout="wide")

st.title("🚜 Sistema de Gestão de Áreas e Safra")

tab1, tab2 = st.tabs(["📍 Mapear Área", "📝 Diário de Campo"])

with tab1:
    st.header("Desenhe o Talhão no Mapa")
    
    # Link do Google Satélite com a atribuição correta para não dar erro
    google_satellite = 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}'
    attr = 'Google'
    
    # Centralizado em Morrinhos/GO (ajuste se preferir)
    m = folium.Map(location=[-17.73, -49.10], zoom_start=14, tiles=google_satellite, attr=attr)
    
    draw = Draw(
        export=True,
        filename='area_fazenda.geojson',
        position='topleft',
        draw_options={
            'polyline': False, 'rectangle': True, 'circle': False, 
            'marker': False, 'circlemarker': False, 'polygon': True,
        }
    )
    draw.add_to(m)
    
    output = st_folium(m, width=900, height=500)
    
    if output and output.get('all_drawings'):
        st.success("Área capturada!")

with tab2:
    st.header("Dados da Cultura e Aplicação")
    with st.form("diario_safra"):
        col1, col2 = st.columns(2)
        with col1:
            cultura = st.text_input("Cultura (Ex: Soja)")
            safra = st.text_input("Ano da Safra")
            adubo = st.text_input("Adubação")
        with col2:
            metodo = st.selectbox("Método", ["Uniport", "Pivô Central", "A Lanço"])
            produto = st.text_input("Produto Químico")
            dose = st.number_input("Quantidade (L ou kg/ha)")
        
        if st.form_submit_button("Salvar Registro"):
            st.balloons()
            st.success("Dados registrados!")
