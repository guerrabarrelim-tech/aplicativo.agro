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
    
    # URL do Google Híbrido (Satélite + Estradas + Nomes em Português)
    # O parâmetro &hl=pt-BR força o idioma para Português do Brasil
    google_hybrid = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}&hl=pt-BR'
    
    # Criando o mapa com a atribuição obrigatória para evitar o ValueError
    m = folium.Map(
        location=[-17.73, -49.10], 
        zoom_start=14, 
        tiles=google_hybrid, 
        attr='Google Maps'
    )
    
    # ADICIONA O BOTÃO DE GPS (LOCALIZAÇÃO INSTANTÂNEA)
    # O texto de ajuda também configurado para PT-BR
    LocateControl(
        auto_start=False,
        strings={"title": "Mostrar minha localização atual", "popup": "Você está aqui"}
    ).add_to(m)
    
    # Ferramentas de desenho
    draw = Draw(
        export=True,
        filename='area_fazenda.geojson',
        position='topleft',
        draw_options={
            'polyline': False, 
            'rectangle': True, 
            'circle': False, 
            'marker': False, 
            'circlemarker': False, 
            'polygon': True,
        }
    )
    draw.add_to(m)
    
    # Exibe o mapa
    output = st_folium(m, width=900, height=500)
    
    if output and output.get('all_drawings'):
        st.success("Área capturada com sucesso!")

with tab2:
    st.header("Dados da Cultura e Aplicação")
    with st.form("diario_safra"):
        col1, col2 = st.columns(2)
        with col1:
            cultura = st.text_input("Cultura (Ex: Soja, Milho)")
            safra = st.text_input("Ano da Safra (Ex: 24/25)")
            adubo = st.text_input("Adubação Utilizada")
        with col2:
            metodo = st.selectbox("Método de Aplicação", ["Uniport", "Pivô Central", "A Lanço"])
            produto = st.text_input("Produto Químico")
            dose = st.number_input("Quantidade por hectare (kg ou L/ha)", min_value=0.0)
            data_app = st.date_input("Data da Aplicação")
        
        if st.form_submit_button("Salvar Registro"):
            st.balloons()
            st.success("Dados registrados no sistema!")
