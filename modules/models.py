
import numpy as np
import pandas as pd
from datetime import date, timedelta

def build_city_status(weather, traffic, unemp):
    """Construye un pequeño 'estado de la ciudad' a partir de los datos recibidos.

    La idea es tener una función clara que traduzca datos en indicadores
    para la UI. Aquí aplicamos lógica sencilla pero extensible.
    """
    temp = weather.get("temp_mean", 18.0)
    rain = weather.get("rain_mm", 0.0)
    today_inc = traffic.get("today_count", 4)
    last_unemp = unemp.get("last_value", 3350)

    # riesgo base
    risk = 0.25

    # la lluvia aumenta riesgo
    if rain > 0:
        risk += min(rain / 20.0, 0.15)  # máx +15 puntos

    # temperaturas extremas también influyen
    if temp < 5 or temp > 35:
        risk += 0.1

    # si hoy hay muchas incidencias (comparado con media supuesta)
    if today_inc >= 6:
        risk += 0.1

    risk = float(np.clip(risk, 0, 1))

    return {
        "risk_today": risk,
        "temp_mean": temp,
        "rain_mm": rain,
        "today_incidents": today_inc,
        "unemployment": last_unemp,
    }

def predict_accident_risk(start_date, horizon, weather, traffic):
    """Genera una serie de riesgo de accidentes para los próximos días.

    Modelo simplificado:
    - base según build_city_status
    - efecto de lluvia (más lluvia => más riesgo)
    - patrón semanal (más riesgo viernes-sábado)
    - un poco de ruido
    """
    if isinstance(start_date, date):
        start = start_date
    else:
        start = start_date.date()

    base_weather = weather.get("rain_mm", 0.0)
    base_rain_factor = min(base_weather / 20.0, 0.15)

    days = [start + timedelta(days=i) for i in range(horizon)]
    risks = []

    for d in days:
        # base
        r = 0.25 + base_rain_factor

        # patrón semanal
        # lunes=0 ... domingo=6
        dow = d.weekday()
        if dow in (4, 5):  # viernes, sábado
            r += 0.08
        elif dow == 6:  # domingo
            r -= 0.03

        # ruido
        r += np.random.normal(0, 0.03)
        r = float(np.clip(r, 0, 1))
        risks.append(r)

    return pd.DataFrame({"Fecha": days, "Riesgo": risks})
