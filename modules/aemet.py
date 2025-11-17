
import requests

def get_weather_today(api_key=None, municipality_id="28013"):
    """Devuelve un pequeño resumen del tiempo previsto para hoy en Arganda.

    Si no hay api_key o hay error al llamar a AEMET, devuelve valores simulados.
    municipality_id debería ser el código de municipio de AEMET/INE (ejemplo: Madrid 28079).
    """
    # Valores por defecto (mock)
    fallback = {"rain_mm": 2.5, "temp_mean": 18.0}

    if not api_key:
        return fallback

    try:
        base = "https://opendata.aemet.es/opendata/api"
        endpoint = f"/prediccion/especifica/municipio/diaria/{municipality_id}"
        url = base + endpoint
        params = {"api_key": api_key}

        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data_url = r.json().get("datos")
        if not data_url:
            return fallback

        pred = requests.get(data_url, timeout=10).json()
        # Estructura típica: lista con un elemento, que contiene 'prediccion' y 'dia'
        dia0 = pred[0]["prediccion"]["dia"][0]

        # Temperatura mínima y máxima prevista
        tmax = float(dia0["temperatura"]["maxima"])
        tmin = float(dia0["temperatura"]["minima"])
        temp_mean = (tmax + tmin) / 2.0

        # Precipitación acumulada aproximada: tomamos primer tramo si existe
        prob_lluvia = dia0.get("probPrecipitacion", [])
        rain_prob = 0.0
        if prob_lluvia:
            # cogemos el máximo de probabilidad, a falta de litros reales
            rain_prob = max(float(x["value"]) for x in prob_lluvia if x.get("value") not in ("", None))

        # aproximación: mm = probabilidad/10 sólo como demo
        rain_mm = rain_prob / 10.0

        return {"rain_mm": rain_mm, "temp_mean": temp_mean}
    except Exception:
        return fallback
