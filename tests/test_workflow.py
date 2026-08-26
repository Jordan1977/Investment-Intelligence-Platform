from src.workflow import infer_risk_profile, target_allocation, audit_client, weighted_score


def test_infer_risk_profile_dynamic():
    assert infer_risk_profile(35, 25, "high", "high") == "dynamic"


def test_target_allocation_sums_to_one():
    t = target_allocation("balanced", 0.18)
    assert abs(sum(t.values()) - 1.0) < 1e-9
    assert t["Cash"] >= 0.18


def test_audit_client_flags_real_estate_concentration():
    alerts = audit_client({"financial_assets": 100_000, "real_estate": 500_000, "cash": 20_000, "debt": 0, "horizon_years": 20, "risk_tolerance": "high"})
    assert any(a["title"] == "Concentration immobilière" for a in alerts)


def test_weighted_score():
    s = weighted_score({"a": 80, "b": 60}, {"a": 0.75, "b": 0.25})
    assert s == 75
