import pandas as pd, numpy as np
def generate_risk_map(n=60):
 base_lat, base_lon=40.300,-3.440
 return pd.DataFrame({'lat': base_lat+np.random.normal(0,0.01,n), 'lon': base_lon+np.random.normal(0,0.01,n), 'riesgo': np.random.rand(n)})
