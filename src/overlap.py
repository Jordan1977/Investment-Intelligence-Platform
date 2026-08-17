from __future__ import annotations
import pandas as pd

def _same(a, b, key):
    x, y = str(a.get(key, "")).strip(), str(b.get(key, "")).strip()
    return bool(x and y and x.lower() == y.lower())

def semantic_overlap(a, b, corr=None):
    score = 0.0
    reasons = []
    weights = [
        ("benchmark", 0.35, "même benchmark"),
        ("category", 0.20, "même catégorie"),
        ("region", 0.15, "même zone"),
        ("sector", 0.15, "même secteur"),
        ("vehicle", 0.05, "même véhicule"),
    ]
    for key, w, label in weights:
        if _same(a, b, key):
            score += w
            reasons.append(label)

    if corr is not None and pd.notna(corr):
        corr_component = max(0.0, min(1.0, float(corr))) * 0.30
        score += corr_component
        if corr >= 0.85:
            reasons.append(f"corrélation {corr:.2f}")

    score = min(1.0, score)
    return score, reasons

def build_overlap_matrix(portfolio, universe, correlation: dict):
    merged = portfolio.merge(universe, on="ticker", how="left", suffixes=("", "_u"))
    if "name_u" in merged.columns and "name" in merged.columns:
        merged["name"] = merged["name"].fillna(merged["name_u"])
    merged = merged[merged["ticker"] != "CASH"].reset_index(drop=True)
    rows = []
    matrix = {t: {} for t in merged["ticker"]}

    for i, a in merged.iterrows():
        for j, b in merged.iterrows():
            if i == j:
                matrix[a["ticker"]][b["ticker"]] = 1.0
                continue
            c = None
            try:
                c = correlation.get(a["ticker"], {}).get(b["ticker"])
            except Exception:
                pass
            score, reasons = semantic_overlap(a, b, c)
            matrix[a["ticker"]][b["ticker"]] = score
            if i < j and score >= 0.55:
                rows.append({
                    "a": a["name"], "b": b["name"],
                    "ticker_a": a["ticker"], "ticker_b": b["ticker"],
                    "overlap_score": float(score),
                    "reasons": ", ".join(reasons) if reasons else "similarité multi-critères"
                })
    rows.sort(key=lambda x: x["overlap_score"], reverse=True)
    return {"matrix": matrix, "pairs": rows}
