import numpy as np, pandas as pd
NON_LISTED={'PRIVATE_EQUITY','SCPI_DEMO','STRUCT_DEMO','CASH'}
def load_live_prices(tickers,period='5y'):
    import yfinance as yf
    valid=[t for t in tickers if t and t not in NON_LISTED]
    raw=yf.download(valid,period=period,auto_adjust=True,progress=False,group_by='column',threads=True)
    if raw.empty: raise RuntimeError('No market data returned')
    if isinstance(raw.columns,pd.MultiIndex): close=raw['Close'] if 'Close' in raw.columns.get_level_values(0) else raw.xs('Close',axis=1,level=0)
    else: close=raw[['Close']].rename(columns={'Close':valid[0]})
    return close.to_frame(valid[0]) if isinstance(close,pd.Series) else close.dropna(how='all')
def generate_demo_prices(tickers,days=1260,seed=42):
    rng=np.random.default_rng(seed); dates=pd.bdate_range(end=pd.Timestamp.today().normalize(),periods=days); common=rng.normal(0,1,len(dates))
    pars={'SWDA.L':(.00035,.010),'VUSA.L':(.00040,.011),'CNDX.L':(.00055,.015),'EMIM.L':(.00025,.013),'IEAC.L':(.00010,.004),'IGLO.L':(.00008,.005),'EXSA.DE':(.00028,.011),'INRG.L':(.00020,.018),'WDSC.L':(.00033,.014),'VHYL.L':(.00028,.009),'IEGA.L':(.00007,.004),'GHYS.L':(.00016,.007),'SGLN.L':(.00024,.010)}
    out={}
    for t in tickers:
        if t in NON_LISTED: continue
        mu,s=pars.get(t,(.00025,.012)); z=.52*common+.854*rng.normal(0,1,len(dates)); rets=np.clip(mu+s*z,-.25,.25); out[t]=100*np.exp(np.cumsum(np.log1p(rets)))
    return pd.DataFrame(out,index=dates)
