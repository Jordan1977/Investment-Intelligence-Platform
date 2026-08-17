import pandas as pd
from src.stress_testing import run_stress_tests

def test_stress_returns_scenarios():
    p = pd.DataFrame([{"name":"A","ticker":"A","weight":1.0}])
    u = pd.DataFrame([{"name":"A","ticker":"A","asset_class":"Equity","currency":"EUR","sector":"Diversified","duration":None}])
    out = run_stress_tests(p,u)
    assert len(out["scenarios"]) >= 4
    assert out["worst_case"]["portfolio_impact"] < 0
