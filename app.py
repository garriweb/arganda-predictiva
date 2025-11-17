
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
import plotly.express as px

from modules.aemet import get_weather_today
from modules.dgt import get_dgt_incidents
from modules.ine import get_unemployment_summary
from modules.models import build_city_status, predict_accident_risk
from modules.risk_map import generate_risk_map

st.set_page_config(
    page_title="Arganda Predictiva",
    layout="wide",
    page_icon="📊"
)

# ---------------------- HEADER ----------------------
st.markdown("<h1 style='text-align:center;'>🔮 Arganda Predictiva</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;color:gray;'>Gemelo digital y predicción urbana basada en datos abiertos</h4>", unsafe_allow_html=True)
st.markdown("---")

# ---------------------- SIDEBAR ----------------------
st.sidebar.title("Panel de control")
today = date.today()
selected_date = st.sidebar.date_input("Fecha de análisis", value=today)
horizon = st.sidebar.slider("Horizonte de predicción (días)", 1, 7, 3)

st.sidebar.markdown("### Capas de datos")
use_aemet = st.sidebar.checkbox("Clima (AEMET)", True)
use_dgt = st.sidebar.checkbox("Tráfico (DGT)", True)
use_ine = st.sidebar.checkbox("Paro (INE)", True)

show_map = st.sidebar.checkbox("Mostrar mapa de riesgo", True)
st.sidebar.markdown("---")
st.sidebar.caption("Demo técnica • Datos reales cuando se configuren las API keys, "
                   "datos simulados mientras tanto.")

# ---------------------- DATA FETCH ----------------------
aemet_key = None
try:
    aemet_key = st.secrets.get("AEMET_KEY", None)
except Exception:
    aemet_key = None

if use_aemet:
    weather = get_weather_today(api_key=aemet_key)
else:
    weather = {"rain_mm": 2.5, "temp_mean": 18.0}

if use_dgt:
    traffic = get_dgt_incidents()
else:
    traffic = {"today_count": 4, "week_avg": 5.2}

if use_ine:
    unemp = get_unemployment_summary()
else:
    unemp = {"last_value": 3350, "series": [], "years": []}

status = build_city_status(weather, traffic, unemp)

# ---------------------- SECTION 1: STATUS ----------------------
st.subheader("📍 Estado actual estimado de Arganda del Rey")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Riesgo tráfico hoy", f"{status['risk_today']*100:.1f} %")
c2.metric("Lluvia (mm)", f"{weather['rain_mm']:.1f}")
c3.metric("Temp. media (ºC)", f"{weather['temp_mean']:.1f}")
c4.metric("Personas en paro", f"{unemp['last_value']:,}".replace(",", "."))

st.caption("Los valores se calculan combinando datos (o simulaciones) de AEMET, DGT e INE.")

st.markdown("---")

# ---------------------- SECTION 2: PREDICTION ----------------------
st.subheader("📈 Predicción de riesgo de accidentes en los próximos días")

forecast_df = predict_accident_risk(selected_date, horizon, weather, traffic)

fig = px.line(
    forecast_df,
    x="Fecha",
    y="Riesgo",
    title="Riesgo de accidente por día",
    markers=True,
    labels={"Riesgo": "Probabilidad estimada"}
)
fig.update_yaxes(range=[0, 1])

st.plotly_chart(fig, use_container_width=True)

st.caption("Modelo simplificado que tiene en cuenta lluvia, temperatura, patrón semanal e intensidad de tráfico.")

# ---------------------- SECTION 3: UNEMPLOYMENT VS TRAFFIC ----------------------
st.subheader("📊 Paro vs incidencias de tráfico (vista exploratoria)")

# Creamos una serie temporal mock tomando el último año
months = pd.date_range(end=selected_date, periods=12, freq="M")
if unemp["series"]:
    # si en el futuro conectas INE de verdad, aquí puedes usar esa serie
    paro = np.array(unemp["series"][-12:])
else:
    paro = np.linspace(3800, 3300, 12) + np.random.normal(0, 40, 12)

traffic_incidents = np.linspace(40, 55, 12) + np.random.normal(0, 4, 12)

df_corr = pd.DataFrame({
    "Mes": months,
    "Paro": paro,
    "Incidencias de tráfico": traffic_incidents
}).set_index("Mes")

fig2 = px.line(
    df_corr,
    y=["Paro", "Incidencias de tráfico"],
    title="Evolución simulada de paro e incidencias de tráfico"
)
st.plotly_chart(fig2, use_container_width=True)

st.caption("Este gráfico sirve para ilustrar cómo explorar relaciones entre paro y tráfico con datos abiertos reales.")

# ---------------------- SECTION 4: RISK MAP ----------------------
if show_map:
    st.subheader("🗺️ Mapa de riesgo de tráfico (simulado)")

    map_df = generate_risk_map(n_points=80)
    st.map(map_df[["lat", "lon"]], zoom=13)

    st.caption("En una versión avanzada, cada punto representaría un cruce o tramo real con riesgo calculado.")

# ---------------------- FOOTER ----------------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:gray;'>"
    "Arganda Predictiva · Prototipo de gemelo digital para concursos de datos abiertos"
    "</p>",
    unsafe_allow_html=True
)
# Creamos una serie temporal mock tomando el último año
months = pd.date_range(end=selected_date, periods=12, freq="M")

# --- FIX: garantizar que paro SIEMPRE tenga 12 valores ---
if unemp["series"] and len(unemp["series"]) >= 12:
    paro = np.array(unemp["series"][-12:])
else:
    paro = np.linspace(3800, 3300, 12) + np.random.normal(0, 40, 12)

# --- FIX: garantizar que traffic_incidents SIEMPRE tenga 12 valores ---
traffic_incidents = np.linspace(40, 55, 12) + np.random.normal(0, 4, 12)

df_corr = pd.DataFrame({
    "Mes": months,
    "Paro": paro,
    "Incidencias de tráfico": traffic_incidents
}).set_index("Mes")
