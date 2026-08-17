from __future__ import annotations
import pandas as pd

def committee_status(row):
    if not bool(row.get("eligible", False)):
        return "Reject", "Critères d'éligibilité non respectés."
    score = row.get("score")
    if pd.isna(score):
        return "Review", "Score incomplet : analyse qualitative nécessaire."
    score = float(score)
    mdd = row.get("max_drawdown")
    ter = row.get("ter")
    if score >= 78 and (pd.isna(mdd) or float(mdd) > -0.35):
        return "Approved", "Profil quantitatif robuste au sein de l'univers."
    if score >= 62:
        return "Watch", "Candidat intéressant, à confirmer par due diligence qualitative."
    return "Review", "Score inférieur au seuil de conviction ; approfondissement requis."

def build_committee_book(scored, limit=18):
    rows = []
    for _, r in scored.head(limit).iterrows():
        status, rationale = committee_status(r)
        rows.append({
            "name": r.get("name"),
            "ticker": r.get("ticker"),
            "asset_class": r.get("asset_class"),
            "vehicle": r.get("vehicle"),
            "score": None if pd.isna(r.get("score")) else float(r.get("score")),
            "status": status,
            "rationale": rationale,
            "ter": None if pd.isna(r.get("ter")) else float(r.get("ter")),
            "sharpe": None if pd.isna(r.get("sharpe")) else float(r.get("sharpe")),
            "max_drawdown": None if pd.isna(r.get("max_drawdown")) else float(r.get("max_drawdown")),
        })
    return rows
