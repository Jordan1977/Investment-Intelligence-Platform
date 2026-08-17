import numpy as np
def trend_score(s):
    s=s.dropna()
    if len(s)<252:return 50.0
    p1=s.iloc[-1]/s.iloc[-63]-1; p3=s.iloc[-1]/s.iloc[-126]-1; p12=s.iloc[-1]/s.iloc[-252]-1; v=s.pct_change().dropna().tail(63).std()*np.sqrt(252)
    return float(max(0,min(100,50+120*p1+80*p3+40*p12-40*v)))
def label(x): return 'Positive' if x>=70 else 'Constructive' if x>=55 else 'Neutral' if x>=40 else 'Fragile' if x>=25 else 'Defensive'
def build_market_monitor(prices,benchmarks):
    out=[]
    for name,t in benchmarks.items():
        if t not in prices: continue
        s=prices[t].dropna(); sc=trend_score(s); r=s.pct_change(fill_method=None).dropna()
        if len(s)<252: continue
        out.append({'label':name,'ticker':t,'score':sc,'regime':label(sc),'perf_1m':float(s.iloc[-1]/s.iloc[-21]-1),'perf_3m':float(s.iloc[-1]/s.iloc[-63]-1),'perf_1y':float(s.iloc[-1]/s.iloc[-252]-1),'volatility':float(r.tail(252).std()*np.sqrt(252))})
    return sorted(out,key=lambda x:x['score'],reverse=True)
