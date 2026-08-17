import numpy as np, pandas as pd
TD=252
def daily_returns(p): return p.pct_change(fill_method=None).dropna()
def cagr(p):
    p=p.dropna(); y=len(p)/TD
    return float((p.iloc[-1]/p.iloc[0])**(1/y)-1) if len(p)>1 and y>0 else np.nan
def vol(r): return float(r.std(ddof=1)*np.sqrt(TD)) if len(r)>1 else np.nan
def sharpe(r,rf=.02):
    v=vol(r); return float((r.mean()*TD-rf)/v) if np.isfinite(v) and v>0 else np.nan
def sortino(r,rf=.02):
    d=r[r<0]; dv=float(d.std(ddof=1)*np.sqrt(TD)) if len(d)>1 else np.nan
    return float((r.mean()*TD-rf)/dv) if np.isfinite(dv) and dv>0 else np.nan
def maxdd(p):
    p=p.dropna(); return float((p/p.cummax()-1).min()) if len(p) else np.nan
def var95(r): return float(np.nanpercentile(r,5)) if len(r) else np.nan
def consistency(r):
    m=(1+r).resample('ME').prod()-1 if len(r) else pd.Series(dtype=float)
    return float((m>0).mean()) if len(m) else np.nan
def rolling_sharpe(r,w=126): return (r.rolling(w).mean()*TD-.02)/(r.rolling(w).std()*np.sqrt(TD)).replace(0,np.nan)
def drawdown_series(p): return p/p.cummax()-1
def compute_metrics(p):
    r=daily_returns(p)
    return {'cagr':cagr(p),'volatility':vol(r),'sharpe':sharpe(r),'sortino':sortino(r),'max_drawdown':maxdd(p),'var95_1d':var95(r),'consistency':consistency(r),'history_days':int(p.dropna().shape[0])}
