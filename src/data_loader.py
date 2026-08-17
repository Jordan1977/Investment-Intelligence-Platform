from pathlib import Path
import pandas as pd
ALIASES={"isin code":"isin","code isin":"isin","nom":"name","libelle":"name","libellé":"name","classe d'actifs":"asset_class","classe actif":"asset_class","catégorie":"category","categorie":"category","frais courants":"ter","encours":"aum_m","encours m€":"aum_m","devise":"currency","score esg":"esg_score"}
def normalize_columns(df):
    return df.rename(columns={c:ALIASES.get(str(c).strip().lower(),str(c).strip().lower().replace(' ','_')) for c in df.columns})
def load_universe(path):
    df=normalize_columns(pd.read_csv(path))
    for c in ['ter','aum_m','esg_score','liquidity_score','qualitative_score','diversification_score']:
        if c in df: df[c]=pd.to_numeric(df[c],errors='coerce')
    return df
def load_portfolio(path):
    df=normalize_columns(pd.read_csv(path))
    df['weight']=pd.to_numeric(df['weight'],errors='coerce').fillna(0)
    t=float(df['weight'].sum())
    if t<=0: raise ValueError('Portfolio weights must sum to a positive number')
    df['weight']/=t
    return df
