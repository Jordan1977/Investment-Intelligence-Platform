def allocation_gap(current,target):
    return [{'asset_class':k,'current':float(current.get(k,0)),'target':float(target.get(k,0)),'gap':float(target.get(k,0)-current.get(k,0))} for k in sorted(set(current)|set(target))]
def candidate_supports(scored,asset_class,limit=3):
    rows=scored[(scored.asset_class==asset_class)&scored.eligible].dropna(subset=['score']).sort_values('score',ascending=False).head(limit)
    return [{'name':r['name'],'ticker':r['ticker'],'score':float(r['score']),'reason':f"Score {r['score']:.0f}/100 • Sharpe {r.get('sharpe',0) if r.get('sharpe')==r.get('sharpe') else 0:.2f} • TER {r.get('ter',0):.2%}"} for _,r in rows.iterrows()]
