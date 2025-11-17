import pandas as pd, numpy as np
def predict_accident_risk(start,h):
 import pandas as pd, numpy as np
 from datetime import timedelta
 dates=pd.date_range(start=start, periods=h)
 risk=np.clip(0.37+np.random.normal(0,0.03,h),0,1)
 return pd.DataFrame({'Fecha':dates,'Riesgo':risk})
