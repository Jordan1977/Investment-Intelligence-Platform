from __future__ import annotations
import pandas as pd

DEFAULT_SCENARIOS = {
    "Equity Shock -20%": {
        "equity": -0.20, "bonds": -0.02, "alternative": -0.06,
        "real_estate": -0.08, "cash": 0.00
    },
    "Rates +200 bps": {
        "equity": -0.08, "bonds": "duration", "alternative": -0.03,
        "real_estate": -0.10, "cash": 0.01, "rate_shock": 0.02
    },
    "Credit Widening": {
        "equity": -0.07, "bonds": -0.05, "alternative": -0.04,
        "real_estate": -0.05, "cash": 0.00
    },
    "EUR Appreciation +10%": {
        "equity": -0.03, "bonds": -0.01, "alternative": -0.02,
        "real_estate": 0.00, "cash": 0.00, "usd_fx": -0.10
    },
    "Global Risk-Off": {
        "equity": -0.25, "bonds": 0.03, "alternative": -0.10,
        "real_estate": -0.12, "cash": 0.00
    },
}

def _base_shock(row, scenario):
    ac = str(row.get("asset_class", "")).lower().replace(" ", "_")
    if ac == "real_estate":
        key = "real_estate"
    elif ac == "bonds":
        key = "bonds"
    elif ac == "equity":
        key = "equity"
    elif ac == "cash":
        key = "cash"
    else:
        key = "alternative"

    shock = scenario.get(key, 0.0)
    if shock == "duration":
        duration = float(row.get("duration") or 0.0)
        shock = -duration * float(scenario.get("rate_shock", 0.0))

    if scenario.get("usd_fx") and str(row.get("currency", "")).upper() == "USD":
        shock += float(scenario["usd_fx"])

    sector = str(row.get("sector", "")).lower()
    if "technology" in sector and scenario.get("equity", 0) < -0.15:
        shock -= 0.04
    if "private equity" in sector and scenario.get("equity", 0) < -0.15:
        shock -= 0.05
    return float(shock)

def run_stress_tests(portfolio: pd.DataFrame, universe: pd.DataFrame, scenarios=None) -> dict:
    scenarios = scenarios or DEFAULT_SCENARIOS
    merged = portfolio.merge(universe, on="ticker", how="left", suffixes=("", "_u"))
    merged.loc[merged["ticker"] == "CASH", ["asset_class", "currency"]] = ["Cash", "EUR"]

    results = []
    for name, scenario in scenarios.items():
        impacts = []
        total = 0.0
        for _, row in merged.iterrows():
            shock = _base_shock(row, scenario)
            contribution = float(row["weight"]) * shock
            impacts.append({
                "name": row["name"],
                "ticker": row["ticker"],
                "weight": float(row["weight"]),
                "shock": shock,
                "contribution": contribution,
            })
            total += contribution
        impacts.sort(key=lambda x: x["contribution"])
        results.append({
            "scenario": name,
            "portfolio_impact": float(total),
            "top_detractors": impacts[:3],
            "top_resilient": sorted(impacts, key=lambda x: x["contribution"], reverse=True)[:3],
        })
    worst = min(results, key=lambda x: x["portfolio_impact"]) if results else None
    return {"scenarios": results, "worst_case": worst}
