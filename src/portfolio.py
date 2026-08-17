import numpy as np, pandas as pd
from .metrics import compute_metrics

def portfolio_returns(returns,weights):
    cols=[c for c in weights.index if c in returns.columns]
    if not cols:return pd.Series(dtype=float)
    w=weights.loc[cols].astype(float); w=w/w.sum(); return returns[cols].mul(w,axis=1).sum(axis=1)

def audit_portfolio(portfolio,universe,prices,alerts):
    m=portfolio.merge(universe,on='ticker',how='left',suffixes=('','_u'))
    m.loc[m.ticker=='CASH',['asset_class','region','sector','ter','liquidity_score']]=['Cash','Cash','Cash',0.0,100]
    returns=prices.pct_change(fill_method=None).dropna(); listed=m[m.ticker.isin(prices.columns)].copy(); w=listed.set_index('ticker').weight if len(listed) else pd.Series(dtype=float)
    pr=portfolio_returns(returns,w); wealth=(1+pr).cumprod() if len(pr) else pd.Series(dtype=float); metrics=compute_metrics(wealth) if len(wealth) else {}
    corrcols=[c for c in w.index if c in returns.columns]; corr=returns[corrcols].corr() if corrcols else pd.DataFrame()
    by_asset=m.groupby('asset_class',dropna=False).weight.sum().to_dict(); by_region=m.groupby('region',dropna=False).weight.sum().to_dict(); by_sector=m.groupby('sector',dropna=False).weight.sum().to_dict()
    weighted_ter=float((m.weight*pd.to_numeric(m.ter,errors='coerce').fillna(0)).sum()); hhi=float((m.weight**2).sum())
    div=max(0,min(100,100*(1-hhi))); cost=max(0,min(100,100*(1-weighted_ter/.02))); risk=max(0,min(100,100*(1-(metrics.get('volatility',0) or 0)/.25))); liq=float((m.weight*pd.to_numeric(m.liquidity_score,errors='coerce').fillna(50)).sum()); health=.35*div+.25*risk+.20*cost+.20*liq
    flags=[]
    if m.weight.max()>alerts['max_single_position_weight']:
        r=m.loc[m.weight.idxmax()]; flags.append({'level':'warning','title':'Concentration ligne','text':f"{r['name']} représente {r['weight']:.0%} du portefeuille."})
    if by_asset.get('Equity',0)>alerts['high_equity_weight']: flags.append({'level':'warning','title':'Budget actions','text':f"La poche actions atteint {by_asset.get('Equity',0):.0%}."})
    if by_region.get('United States',0)>alerts['high_us_weight']: flags.append({'level':'warning','title':'Exposition États-Unis','text':f"L'exposition directe identifiée atteint {by_region.get('United States',0):.0%}."})
    GENERIC_SECTOR_LABELS={'Diversified','Fixed Income','Real Estate','Private Equity','Structured','Cash'}
    real_sectors={k:v for k,v in by_sector.items() if k not in GENERIC_SECTOR_LABELS}
    if real_sectors and max(real_sectors.values())>alerts['high_sector_weight']:
        s=max(real_sectors,key=real_sectors.get); flags.append({'level':'info','title':'Concentration sectorielle','text':f"{s} représente {real_sectors[s]:.0%} du portefeuille (hors expositions diversifiées)."})
    if weighted_ter>alerts['high_weighted_ter']: flags.append({'level':'warning','title':'Coût du portefeuille','text':f"TER pondéré estimé : {weighted_ter:.2%}."})
    high=[]
    for i in range(len(corr.columns)):
        for j in range(i+1,len(corr.columns)):
            v=corr.iloc[i,j]
            if pd.notna(v) and v>=alerts['high_pair_correlation']: high.append({'a':corr.columns[i],'b':corr.columns[j],'correlation':float(v)})
    if high:
        p=max(high,key=lambda x:x['correlation']); flags.append({'level':'info','title':'Corrélation élevée','text':f"{p['a']} et {p['b']} : {p['correlation']:.2f}."})
    if not flags: flags=[{'level':'success','title':'Contrôles de seuil','text':'Aucune alerte majeure détectée avec la configuration actuelle.'}]
    rc={}
    if len(corrcols):
        ww=w.loc[corrcols]; ww=ww/ww.sum(); cov=returns[corrcols].cov()*252; pv=float(np.sqrt(ww.values@cov.values@ww.values))
        if pv>0:
            vals=ww.values*(cov.values@ww.values)/pv; rc={k:float(v) for k,v in zip(corrcols,vals)}
    return {'metrics':metrics,'health_score':float(health),'diversification_score':float(div),'risk_score':float(risk),'cost_score':float(cost),'liquidity_score':float(liq),'weighted_ter':weighted_ter,'allocation_asset':{str(k):float(v) for k,v in by_asset.items()},'allocation_region':{str(k):float(v) for k,v in by_region.items()},'allocation_sector':{str(k):float(v) for k,v in by_sector.items()},'flags':flags,'correlation':corr.round(3).fillna(0).to_dict(),'risk_contribution':rc,'wealth':[{'date':d.strftime('%Y-%m-%d'),'value':float(v)} for d,v in wealth.iloc[-756:].items()]}
