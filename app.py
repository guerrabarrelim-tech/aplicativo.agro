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
    
    # Google Híbrido (Satélite + Estradas em Português)
    # O parâmetro &hl=pt-BR coloca os nomes em português
    google_hybrid = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}&hl=pt-BR'
    
    # CRIANDO O MAPA - Note o 'attr' que evita o erro que você está tendo
    m = folium.Map(
        location=[-17.73, -49.10], 
        zoom_start=14, 
        tiles=google_hybrid, 
        attr='Google Maps'
    )
    
    # Botão de GPS (Localização Instantânea)
    LocateControl(
        auto_start=False,
        strings={"title": "Minha Localização", "popup": "Você está aqui"}
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
    
    # Exibe o mapa
    st_folium(m, width=900, height=500)

with tab2:
    st.header("Dados da Cultura e Aplicação")
    
    with st.form("diario_safra"):
        col1, col2 = st.columns(2)
        
        with col1:
            cultura = st.selectbox("Cultura", ["Soja", "Milho", "Algodão", "Feijão", "Sorgo", "Outra"])
            cultivar = st.text_input("Variedade / Cultivar (Ex: M7739 IPRO)")
            safra = st.text_input("Safra (Ex: 2024/25)")
            data_app = st.date_input("Data da Aplicação")
            
        with col2:
            metodo = st.selectbox("Método de Aplicação", ["Uniport", "Pivô Central", "A Lanço", "Costal", "Tratorizado"])
            
            st.write("**Mistura de Calda (Produtos):**")
            # Aqui você pode adicionar quantos produtos quiser
            produtos = st.text_area("Liste os produtos e dosagens", 
                                  placeholder="Ex:\n1. Glifosato - 2L/ha\n2. Óleo Mineral - 0.5L/ha\n3. Inseticida - 0.3L/ha")
            
        if st.form_submit_button("Salvar Registro"):
            st.balloons()
            st.success(f"Registro de {cultura} ({cultivar}) salvo!")
