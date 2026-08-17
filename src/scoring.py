import numpy as np, pandas as pd
def percentile_score(s,higher=True):
    p=pd.to_numeric(s,errors='coerce').rank(pct=True,method='average'); p= p if higher else 1-p; return (p*100).fillna(50)
def apply_eligibility(df,rules):
    out=df.copy(); out['eligible']=True
    listed=out['ticker'].str.contains(r'\.',regex=True,na=False)
    if 'history_days' in out: out.loc[listed&(out['history_days']<rules.get('min_history_days',0)),'eligible']=False
    out.loc[out['aum_m'].fillna(0)<rules.get('min_aum_m',0),'eligible']=False
    for i,r in out.iterrows():
        cap=rules['max_ter'].get(r['asset_class'],rules['max_ter']['default'])
        if pd.notna(r['ter']) and r['ter']>cap: out.at[i,'eligible']=False
    return out
def score_group(df,weights):
    out=df.copy(); mapping={'perf_3y':('cagr',1),'perf_1y':('perf_1y',1),'sharpe':('sharpe',1),'sortino':('sortino',1),'max_drawdown':('max_drawdown',1),'volatility':('volatility',0),'consistency':('consistency',1),'cost':('ter',0),'aum':('aum_m',1),'esg':('esg_score',1),'qualitative':('qualitative_score',1),'liquidity':('liquidity_score',1),'diversification':('diversification_score',1)}
    total=pd.Series(0.0,index=out.index); used=0
    for k,w in weights.items():
        src,high=mapping[k]
        if src not in out: continue
        out['score_'+k]=percentile_score(out[src],bool(high)); total+=w*out['score_'+k]; used+=w
    out['score']=total/used if used else 50; out.loc[~out['eligible'],'score']=np.nan; return out
def explain_score(row):
    return sorted([{'metric':c[6:].replace('_',' ').title(),'score':float(v)} for c,v in row.items() if str(c).startswith('score_') and pd.notna(v)],key=lambda x:x['score'],reverse=True)
