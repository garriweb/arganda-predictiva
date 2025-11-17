
import pandas as pd
import numpy as np

def generate_risk_map(n_points=80):
    """Genera puntos simulados alrededor de Arganda con un nivel de riesgo.

    En una versión real:
    - cada punto sería un tramo o cruce con lat/lon real
    - el campo 'riesgo' vendría del modelo predictivo
    """
    base_lat, base_lon = 40.300, -3.440

    lats = base_lat + np.random.normal(0, 0.01, n_points)
    lons = base_lon + np.random.normal(0, 0.01, n_points)
    risks = np.random.rand(n_points)

    df = pd.DataFrame({
        "lat": lats,
        "lon": lons,
        "riesgo": risks
    })
    return df
