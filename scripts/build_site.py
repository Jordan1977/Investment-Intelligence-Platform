from pathlib import Path
import argparse,json,sys,yaml,pandas as pd
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from src.data_loader import load_universe,load_portfolio
from src.market_data import load_live_prices,generate_demo_prices
from src.metrics import compute_metrics,daily_returns,rolling_sharpe,drawdown_series
from src.scoring import apply_eligibility,score_group,explain_score
from src.portfolio import audit_portfolio
from src.advisory import allocation_gap,candidate_supports
from src.market_intelligence import build_market_monitor
from src.stress_testing import run_stress_tests
from src.overlap import build_overlap_matrix
from src.suitability import suitability_assessment
from src.investment_committee import build_committee_book
from src.structured_lab import structured_scenarios
from src.private_markets import private_market_snapshot

def safe(v):
    if v is None:return None
    try:
        if pd.isna(v):return None
    except Exception:pass
    return v.item() if hasattr(v,'item') else v

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--demo',action='store_true'); ap.add_argument('--live',action='store_true'); args=ap.parse_args()
    scoring=yaml.safe_load((ROOT/'config/scoring.yml').read_text(encoding='utf-8')); profiles=yaml.safe_load((ROOT/'config/profiles.yml').read_text(encoding='utf-8')); marketcfg=yaml.safe_load((ROOT/'config/market.yml').read_text(encoding='utf-8'))
    universe=load_universe(ROOT/'data/universe.csv'); tickers=universe.ticker.dropna().tolist()
    try:
        prices=load_live_prices(tickers) if args.live and not args.demo else generate_demo_prices(tickers); mode='live' if args.live and not args.demo else 'demo'
    except Exception as e:
        print('[WARN] live data failed:',e); prices=generate_demo_prices(tickers); mode='demo-fallback'
    rows=[]; deep={}
    for _,row in universe.iterrows():
        t=row.ticker; rec=row.to_dict()
        if t in prices:
            s=prices[t].dropna(); rec.update(compute_metrics(s)); rec['perf_1y']=float(s.iloc[-1]/s.iloc[-252]-1) if len(s)>=252 else None; r=daily_returns(s); rs=rolling_sharpe(r); dd=drawdown_series(s); base=max(0,len(s)-756); idx=list(range(base,len(s),5))
            deep[t]={'price':[{'date':s.index[i].strftime('%Y-%m-%d'),'value':float(s.iloc[i]/s.iloc[base]*100)} for i in idx],'drawdown':[{'date':dd.index[i].strftime('%Y-%m-%d'),'value':float(dd.iloc[i])} for i in idx if i<len(dd)],'rolling_sharpe':[{'date':d.strftime('%Y-%m-%d'),'value':float(v)} for d,v in rs.dropna().iloc[-756::5].items()]}
        else: rec.update({'cagr':None,'volatility':None,'sharpe':None,'sortino':None,'max_drawdown':None,'var95_1d':None,'consistency':None,'history_days':0,'perf_1y':None})
        rows.append(rec)
    df=apply_eligibility(pd.DataFrame(rows),scoring['eligibility']); parts=[]
    for ac,g in df.groupby('asset_class',dropna=False): parts.append(score_group(g,scoring['weights'].get(ac,scoring['weights']['Alternative'])))
    scored=pd.concat(parts,ignore_index=True); scored['score_explanation']=scored.apply(explain_score,axis=1); scored=scored.sort_values('score',ascending=False,na_position='last')
    portfolio=load_portfolio(ROOT/'data/sample_portfolios/balanced.csv'); audit=audit_portfolio(portfolio,universe,prices,scoring['alerts']); enriched=portfolio.merge(universe[['ticker','asset_class']],on='ticker',how='left'); enriched.loc[enriched.ticker=='CASH','asset_class']='Cash'; current=enriched.groupby('asset_class').weight.sum().to_dict()
    advisory={}
    for key,p in profiles['client_profiles'].items():
        gaps=allocation_gap(current,p['target']); cand={}
        for g in gaps:
            if g['gap']>.01: cand[g['asset_class']]=candidate_supports(scored,g['asset_class'])
        advisory[key]={'label':p['label'],'risk_budget':p['risk_budget'],'gaps':gaps,'candidates':cand}
    market=build_market_monitor(prices,marketcfg['benchmarks'])
    stress=run_stress_tests(portfolio,universe)
    overlap=build_overlap_matrix(portfolio,universe,audit.get('correlation',{}))
    suitability={}
    for key,p in profiles['client_profiles'].items():
        suitability[key]=suitability_assessment(audit,current,p)
    committee=build_committee_book(scored)
    structured={}
    for _,r in universe[universe['vehicle']=='Structured Product'].iterrows():
        structured[r['ticker']]=structured_scenarios(r.to_dict())
    private_markets=private_market_snapshot(universe)
    data_quality={
        'universe_rows':int(len(universe)),
        'missing_ticker':int(universe['ticker'].isna().sum()),
        'missing_isin':int(universe['isin'].isna().sum()),
        'missing_aum':int(universe['aum_m'].isna().sum()),
        'missing_ter':int(universe['ter'].isna().sum()),
        'duplicate_tickers':int(universe['ticker'].duplicated().sum()),
        'completeness':float(1-universe[['name','ticker','asset_class','vehicle','ter','aum_m']].isna().mean().mean())
    }
    payload={'meta':{'generated_at':pd.Timestamp.now(tz='UTC').isoformat(),'mode':mode,'universe_count':int(len(scored)),'eligible_count':int(scored.eligible.sum()),'version':'V11 Advisory Workflow'},'universe':[{k:safe(v) for k,v in r.items()} for r in scored.to_dict('records')],'deepdive':deep,'portfolio':{'holdings':portfolio.to_dict('records'),'audit':audit,'stress':stress,'overlap':overlap},'advisory':advisory,'suitability':suitability,'committee':committee,'structured_lab':structured,'private_markets':private_markets,'data_quality':data_quality,'market':market}
    out=ROOT/'docs/data/dashboard.json'; out.write_text(json.dumps(payload,ensure_ascii=False,allow_nan=False,indent=2),encoding='utf-8')
    import shutil
    demo_src=ROOT/'data/demo'; demo_dst=ROOT/'docs/data/demo'
    if demo_src.exists():
        shutil.rmtree(demo_dst, ignore_errors=True); shutil.copytree(demo_src, demo_dst)
    print(f'Built {mode} dashboard with {len(scored)} instruments')
if __name__=='__main__':main()
