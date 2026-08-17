import pandas as pd
from src.metrics import compute_metrics
def test_metrics_smoke():
    idx=pd.bdate_range('2024-01-01',periods=600); s=pd.Series([100*(1.0003**i) for i in range(600)],index=idx); m=compute_metrics(s); assert m['history_days']==600; assert m['max_drawdown']<=1e-9
