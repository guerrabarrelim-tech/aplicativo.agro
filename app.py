import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import Draw, LocateControl

# Configuração da página
st.set_page_config(page_title="Gestor de Safra Pro", layout="wide")

st.title("🚜 Sistema de Gestão de Áreas e Safra")

tab1, tab2 = st.tabs(["📍 Mapear Área", "📝 Diário de Campo"])

with tab1:
    st.header("Localização e Desenho")
    
    # URL do Google Híbrido (Satélite + Estradas + Nomes em PT-BR)
    # Importante: attr='Google' resolve o erro de Attribution
    google_hybrid = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}&hl=pt-BR'
    
    m = folium.Map(
        location=[-17.73, -49.10], 
        zoom_start=14, 
        tiles=google_hybrid, 
        attr='Google Maps'
    )
    
    # Botão de GPS
    LocateControl(
        auto_start=False,
        strings={"title": "Mostrar minha localização", "popup": "Você está aqui"}
    ).add_to(m)
    
    # Ferramentas de desenho
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

with tab2:
    st.header("Dados da Cultura e Aplicação")
    
    with st.form("diario_safra"):
        col1, col2 = st.columns(2)
        
        with col1:
            cultura = st.selectbox("Cultura", ["Soja", "Milho", "Algodão", "Feijão", "Outro"])
            cultivar = st.text_input("Variedade / Cultivar (Ex: M7739 IPRO)")
            safra = st.text_input("Safra (Ex: 24/25)")
            data_app = st.date_input("Data da Aplicação")
            
        with col2:
            metodo = st.selectbox("Método de Aplicação", ["Uniport", "Pivô Central", "A Lanço", "Tratorizado"])
            st.write("**Produtos Utilizados na Calda:**")
            # Campo de texto grande para múltiplos produtos
            produtos_lista = st.text_area("Liste os produtos e doses (Ex: Glifosato 2L + Adjuvante 0.5L)", 
                                         help="Você pode listar todos os produtos da mistura aqui.")
            
        if st.form_submit_button("Salvar Registro"):
            st.balloons()
            st.success(f"Registro de {cultura} ({cultivar}) salvo com sucesso!")
            st.info(f"Produtos registrados: {produtos_lista}")
