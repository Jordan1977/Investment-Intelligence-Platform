import pandas as pd
from src.overlap import build_overlap_matrix

def test_overlap_detects_same_benchmark():
    p=pd.DataFrame([
        {"name":"A","ticker":"A","weight":0.5},
        {"name":"B","ticker":"B","weight":0.5},
    ])
    u=pd.DataFrame([
        {"name":"A","ticker":"A","benchmark":"X","category":"US","region":"US","sector":"Diversified","vehicle":"ETF"},
        {"name":"B","ticker":"B","benchmark":"X","category":"US","region":"US","sector":"Diversified","vehicle":"ETF"},
    ])
    out=build_overlap_matrix(p,u,{"A":{"B":0.95},"B":{"A":0.95}})
    assert out["pairs"]
    assert out["pairs"][0]["overlap_score"] >= 0.55
