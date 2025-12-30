import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import Draw, LocateControl, MeasureControl
import pandas as pd

# Configuração da página
st.set_page_config(page_title="AgroGPS - Medição de Talhões", layout="wide")

st.title("🚜 AgroGPS: Mapeamento e Medição")

tab1, tab2 = st.tabs(["📍 Mapear e Medir", "📝 Registro de Safra"])

with tab1:
    st.header("Medição de Área")
    st.write("Dica: Use o ícone de 'Polígono' à esquerda para desenhar ou caminhe com o GPS ligado.")

    # URL Google Híbrido com PT-BR
    google_hybrid = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}&hl=pt-BR'
    
    # Inicia o mapa (Centralizado na sua região atual)
    m = folium.Map(
        location=[-17.73, -49.10], 
        zoom_start=15, 
        tiles=google_hybrid, 
        attr='Google Maps'
    )

    # 1. BOTÃO DE GPS: Fundamental para você se ver no mapa enquanto anda
    LocateControl(
        auto_start=False,
        strings={"title": "Minha Posição Atual", "popup": "Você está aqui"}
    ).add_to(m)

    # 2. FERRAMENTA DE MEDIÇÃO: Dá distância e área em tempo real
    m.add_child(MeasureControl(
        position='topleft',
        primary_length_unit='meters',
        secondary_length_unit='kilometers',
        primary_area_unit='sqmeters',
        secondary_area_unit='hectares'
    ))

    # 3. FERRAMENTA DE DESENHO: Para marcar o talhão
    draw = Draw(
        export=True,
        filename='talhao_fazenda.geojson',
        position='topleft',
        draw_options={
            'polyline': True,
            'rectangle': True,
            'circle': False,
            'marker': True,
            'polygon': True,
        }
    )
    draw.add_to(m)

    # Exibe o mapa no Streamlit
    output = st_folium(m, width=1000, height=600)

    # Lógica de Cálculo de Área
    if output and output.get('all_drawings'):
        # Tenta pegar a área do último desenho
        st.subheader("📊 Resultados da Área Selecionada")
        
        # Como o cálculo exato de hectares via GeoJSON precisa de bibliotecas pesadas,
        # o MeasureControl (na régua do mapa) é o mais preciso para você ver na hora.
        st.info("Utilize a ferramenta de 'Régua' (Measure) no canto superior esquerdo para ver o cálculo exato em Hectares enquanto desenha.")
        
        # Conversor Simples para consulta
        st.write("---")
        st.write("**Calculadora de Conversão:**")
        valor_ha = st.number_input("Digite o valor em Hectares (ha) para converter:", min_value=0.0)
        if valor_ha > 0:
            alqueire_goiano = valor_ha / 4.84
            st.success(f"Área: {valor_ha} ha | Equivalente a: {alqueire_goiano:.2f} Alqueires (Goiás)")

with tab2:
    st.header("📝 Diário de Campo")
    with st.form("registro"):
        cultura = st.selectbox("Cultura", ["Soja", "Milho", "Outra"])
        cultivar = st.text_input("Variedade/Cultivar")
        area_total = st.number_input("Tamanho da Área (ha)", min_value=0.0)
        produtos = st.text_area("Produtos e Doses (Multi-seleção)")
        
        if st.form_submit_button("Salvar Dados"):
            st.balloons()
            st.success(f"Talhão de {cultivar} registrado!")
