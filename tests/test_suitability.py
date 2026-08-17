from src.suitability import suitability_assessment

def test_suitability_score_range():
    audit={"metrics":{"volatility":0.10},"liquidity_score":90,"cost_score":85,"diversification_score":80}
    profile={"risk_budget":0.13,"target":{"Equity":0.5,"Bonds":0.3,"Cash":0.2}}
    out=suitability_assessment(audit,{"Equity":0.5,"Bonds":0.3,"Cash":0.2},profile)
    assert 0 <= out["score"] <= 100
    assert out["status"] == "Compatible"
