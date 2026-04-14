import streamlit as st
import folium
import time
import random
from streamlit_folium import st_folium
from logic.bus_engine import init_buses, move_buses

# Configuración de página
st.set_page_config(page_title="Movi Rosario | Minimal", layout="centered")

# --- CSS PERSONALIZADO (Estética Minimalista) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    .stButton > button {
        background-color: #000000;
        color: #ffffff;
        border-radius: 4px;
        border: none;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #333333;
        color: #ffffff;
    }
    h1, h2, h3 { color: #000000 !important; }
    .stCaption { color: #666666 !important; }
</style>
""", unsafe_allow_html=True)

# --- ESTADO DE SESIÓN ---
if "screen" not in st.session_state:
    st.session_state.screen = "home"
if "buses" not in st.session_state:
    st.session_state.buses = []

# --- PANTALLA DE INICIO ---
if st.session_state.screen == "home":
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.title("🚌 Movi Rosario")
    st.caption("Sistema de Monitoreo en Tiempo Real")
    st.write("Visualiza el transporte público con una interfaz limpia y eficiente.")
    
    if st.button("Explorar Mapa"):
        st.session_state.buses = init_buses()
        st.session_state.screen = "map"
        st.rerun()

# --- PANTALLA DEL MAPA ---
elif st.session_state.screen == "map":
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Inicio"):
            st.session_state.screen = "home"
            st.rerun()
    with col2:
        st.subheader("Mapa en Tiempo Real")

    # Selección de Línea
    linea = st.selectbox("Línea seleccionada:", ["101", "102", "103", "110", "131", "142", "Enlace Sur"])
    
    # Actualización de posiciones
    st.session_state.buses = move_buses(st.session_state.buses)

    # Crear Mapa (Tiles minimalistas: cartodbpositron)
    center_lat, center_lon = -32.9442, -60.6505
    m = folium.Map(location=[center_lat, center_lon], zoom_start=13, tiles="cartodbpositron")

    for b in st.session_state.buses:
        folium.Marker(
            [b["lat"], b["lon"]],
            popup=f"Línea {linea} - Unidad #{b['id']}",
            icon=folium.Icon(color="black", icon="bus", prefix="fa")
        ).add_to(m)

    # Renderizar Mapa
    st_folium(m, width=700, height=450, returned_objects=[])

    st.divider()
    
    if st.button("⏱️ Consultar Tiempo de Llegada"):
        minutos = random.randint(2, 15)
        st.toast(f"Próxima unidad de la línea {linea} en {minutos} minutos.", icon="🕒")

    # Auto-refresh cada 4 segundos
    time.sleep(4)
    st.rerun()
